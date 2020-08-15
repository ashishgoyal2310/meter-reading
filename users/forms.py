from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        value = self.cleaned_data.get('email')
        if not value:
            raise forms.ValidationError('Email is required.')
        return value