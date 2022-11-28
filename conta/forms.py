from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha'
    )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label = 'Usuário',
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Digite seu usuário'
            }
        ),
        help_text=('Digite seu usuário')
    )

    email = forms.EmailField(
        label = 'E-mail',
        required = True,
    )

    password = forms.CharField(
        label = 'Senha',
        widget= forms.PasswordInput(
            attrs={'placeholder': 'Digite sua senha'}
        )
    )

    password2 = forms.CharField(
        label = 'Confirmação de senha',
        widget= forms.PasswordInput(
            attrs={'placeholder': 'Confirme sua senha'}
        ),
        error_messages={'required': 'Por favor, repita sua senha'}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError('Você precisa confirmar sua senha')
        if password1 != password2:
            raise forms.ValidationError('As senhas não são iguais.')

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O email informado já está em uso',
                code='Invalid',
            )
        
        return email