from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha'
    )


class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]