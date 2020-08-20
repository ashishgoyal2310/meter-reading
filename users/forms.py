from django import forms
from django.contrib.auth import authenticate

from accounts.models import UserAuthToken
from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            obj, created = UserAuthToken.objects.get_or_create(user=user,
                defaults={'token':UserAuthToken.generate_unique_key()})

        return user


class UserResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password = data.get('password', '')
        repeat_password = data.get('repeat_password', '')
        if not (password and repeat_password and password == repeat_password):
            raise forms.ValidationError({'password': 'Invalid password'})


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        value = self.cleaned_data.get('email')
        if not value:
            raise forms.ValidationError('Email is required.')
        return value