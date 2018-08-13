from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=250, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'location',
            'birth_date',
            'phone'
        )
