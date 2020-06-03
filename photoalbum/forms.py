from django import forms
from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email ')
    password = forms.CharField(label='Hasło ', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    email = forms.EmailField(label="Twój email ")
    username = forms.CharField(label="Twój nick ")
    password = forms.CharField(label='Hasło ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło ', widget=forms.PasswordInput)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', "first_name"]


class PasswordViewForm(forms.Form):
    password = forms.CharField(label='Hasło ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło ', widget=forms.PasswordInput)


class AddCommentToPhotoForm(forms.Form):
    comment = forms.CharField(label="Dopisz komentarz do tego zdjęcia", max_length=256)

