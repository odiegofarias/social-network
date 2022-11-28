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
        )
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
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas são diferentes',
                code='Invalid'
            )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                    # Colocarei uma lista de erros futuramente
                ]
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O email informado já está em uso',
                code='Invalid',
            )
        
        return email