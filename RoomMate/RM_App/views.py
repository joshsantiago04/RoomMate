from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms  import AuthenticationForm
from django.db.models import Q

from .models import UserProfile, Preference, MatchRequest
from .forms import UserRegisterForm, UserProfileForm, PreferenceForm, CustomLoginForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        user_form    = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful! Now set your preferences.")
            return redirect('set_preferences')
        else:
            # ← add this so you actually see why it failed
            messages.error(request, "Please correct the errors below.")
    else:
        user_form    = UserRegisterForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
    })
    
def user_login(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = CustomLoginForm()  # Use the new form with placeholders

    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")  # Redirect to home after logging out

@login_required
def set_preferences(request):
    # Get the logged-in user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Try to fetch existing preferences
    try:
        pref_obj = Preference.objects.get(user=user_profile)
    except Preference.DoesNotExist:
        pref_obj = None

    if request.method == 'POST':
        profile_form    = UserProfileForm(request.POST, instance=user_profile)
        preference_form = PreferenceForm(request.POST, instance=pref_obj)

        if profile_form.is_valid() and preference_form.is_valid():
            # Save profile first
            profile_form.save()
            # Then save preference, linking to profile
            pref = preference_form.save(commit=False)
            pref.user = user_profile
            pref.save()
            
    else:
        profile_form    = UserProfileForm(instance=user_profile)
        preference_form = PreferenceForm(instance=pref_obj)

    return render(request, 'preferences.html', {
        'profile_form':    profile_form,
        'preference_form': preference_form,
    })

@login_required
def find_matches(request):
    # 1. Fetch current user's profile and preference
    user_profile = UserProfile.objects.get(user=request.user)
    try:
        user_preference = Preference.objects.get(user=user_profile)
    except Preference.DoesNotExist:
        messages.error(request, "Please set your preferences first.")
        return redirect('set_preferences')

    # 2. Compute matching scores
    potential_matches = UserProfile.objects.exclude(id=user_profile.id)
    matches = []
    for potential in potential_matches:
        try:
            pref = Preference.objects.get(user=potential)
        except Preference.DoesNotExist:
            continue

        # simple 4-point score
        score = (
            (pref.smoking == user_preference.smoking)
            + (pref.pets == user_preference.pets)
            + (pref.noise_level == user_preference.noise_level)
            + (pref.sleep_schedule == user_preference.sleep_schedule)
        )
        if score >= 1:  # threshold
            matches.append({
                'profile':    potential,
                'preference': pref,
                'score':      score * 25,  # convert to %
            })

    # 3. Which profile-IDs have you sent/received unconfirmed requests?
    sent_requests = MatchRequest.objects.filter(
        from_user=request.user,
        is_confirmed=False
    ).values_list('to_user__userprofile__id', flat=True)

    received_requests = MatchRequest.objects.filter(
        to_user=request.user,
        is_confirmed=False
    ).values_list('from_user__userprofile__id', flat=True)

    # 4. Which profile-IDs are mutual confirmed?
    confirmed_qs = MatchRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        is_confirmed=True
    )
    mutual_confirmed = []
    for req in confirmed_qs:
        other_user = req.to_user if req.from_user == request.user else req.from_user
        # check that other_user also confirmed back
        if MatchRequest.objects.filter(
               from_user=other_user,
               to_user=request.user,
               is_confirmed=True
           ).exists():
            # add the profile.id of that User
            other_profile = UserProfile.objects.get(user=other_user)
            mutual_confirmed.append(other_profile.id)

    # 5. Render with all four context lists
    return render(request, 'matches.html', {
        'matches':           matches,
        'sent_requests':     list(sent_requests),
        'received_requests': list(received_requests),
        'mutual_confirmed':  mutual_confirmed,
    })


@login_required
def send_match_request(request, to_user_id):
    other = get_object_or_404(User, id=to_user_id)
    MatchRequest.objects.get_or_create(
        from_user=request.user,
        to_user=other
    )
    return redirect('find_matches')

@login_required
def confirm_match(request, from_user_id):
    other = get_object_or_404(User, id=from_user_id)
    req = get_object_or_404(
        MatchRequest,
        from_user=other,
        to_user=request.user
    )
    req.is_confirmed = True
    req.save()
    return redirect('my_matches')

@login_required
def unsend_match_request(request, to_user_id):
    other = get_object_or_404(User, id=to_user_id)
    MatchRequest.objects.filter(
        from_user=request.user,
        to_user=other,
        is_confirmed=False
    ).delete()
    return redirect('find_matches')

@login_required
def my_matches(request):
    """
    Show only those users for whom there is a mutually-confirmed MatchRequest.
    """
    # All confirmed requests involving me
    confirmed_qs = MatchRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        is_confirmed=True
    )

    mutual = []
    for mr in confirmed_qs:
        other = mr.to_user if mr.from_user == request.user else mr.from_user
        # Ensure the reverse has also been confirmed
        if MatchRequest.objects.filter(
               from_user=other,
               to_user=request.user,
               is_confirmed=True
           ).exists():
            mutual.append(other)

    return render(request, 'my_matches.html', {
        'mutual_matches': mutual
    })
    
@login_required
def unmatch_user(request, uid):
    other = get_object_or_404(User, id=uid)
    # delete both sides of the confirmed match
    MatchRequest.objects.filter(from_user=request.user,   to_user=other, is_confirmed=True).delete()
    MatchRequest.objects.filter(from_user=other, to_user=request.user, is_confirmed=True).delete()
    return redirect('my_matches')