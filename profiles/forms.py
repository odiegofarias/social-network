from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário', 
    )
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
        )
