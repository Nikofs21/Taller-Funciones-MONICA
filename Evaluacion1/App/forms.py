from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa una contraseña segura'}),
        label="Contraseña",
        help_text="Debe tener al menos 8 caracteres, incluyendo una mayúscula y un número."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingresa tu apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'}),
            'username': forms.TextInput(attrs={'placeholder': 'Crea un nombre de usuario'}),
        }
        help_texts = {
            'username': None,  # Elimina el mensaje predeterminado
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula y un número."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        # Sobrescribimos el método save para cifrar la contraseña
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Cifra la contraseña
        if commit:
            user.save()
        return user