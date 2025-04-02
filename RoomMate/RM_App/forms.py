from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Preference

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'bio']

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['smoking', 'pets', 'noise_level', 'sleep_schedule']