from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Preference
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):

    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Age"}),
        label="Age"
    )

    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Gender"
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', 'rows': 3}),
        label="Bio"
    )
    
    
    instagram_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram URL'}),
        label="Instagram"
    )
    
    snapchat_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Snapchat URL'}),
        label="Snapchat"
    )
    
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'bio', 'instagram_link', 'snapchat_link']

class PreferenceForm(forms.ModelForm):
    smoking = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Smoking"
    )
    
    pets = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Pets"
    )
    
    noise_level = forms.ChoiceField(
        choices=Preference._meta.get_field('noise_level').choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Noise Level"
    )
    
    sleep_schedule = forms.ChoiceField(
        choices=Preference._meta.get_field('sleep_schedule').choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Sleep Schedule"
    )

    class Meta:
        model = Preference
        fields = ['smoking', 'pets', 'noise_level', 'sleep_schedule']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
