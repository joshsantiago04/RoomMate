from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserProfileForm, PreferenceForm
from .models import UserProfile, Preference, Match
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('set_preferences')
    else:
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirect to home or dashboard
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("home")  # Redirect to home after logging out

def set_preferences(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = user_profile
            preference.save()
            return redirect('find_matches')
    else:
        form = PreferenceForm()
    return render(request, 'preferences.html', {'form': form})

def find_matches(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_preference = Preference.objects.get(user=user_profile)
    potential_matches = UserProfile.objects.exclude(id=user_profile.id)
    
    matches = []
    for potential in potential_matches:
        preference = Preference.objects.get(user=potential)
        score = 0
        if preference.smoking == user_preference.smoking:
            score += 1
        if preference.pets == user_preference.pets:
            score += 1
        if preference.noise_level == user_preference.noise_level:
            score += 1
        if preference.sleep_schedule == user_preference.sleep_schedule:
            score += 1
        
        if score >= 2:  # Only consider a match if at least 2 preferences align
            matches.append((potential, score))
    
    matches.sort(key=lambda x: x[1], reverse=True)
    return render(request, 'matches.html', {'matches': matches})