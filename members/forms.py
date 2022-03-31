from django.contrib.auth.models import User
from django import forms
from .models import Client


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']


class ClientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'gender', 'photo')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'photo', 'gender')
