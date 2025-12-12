from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError

User = CustomUser
# ==================================================================================
# FORMULARIO DE REGISTRO PERSONALIZADO (VERSIÓN CORREGIDA Y ROBUSTA)
# ==================================================================================
# La `KeyError` que viste nos enseñó que modificar campos heredados en `__init__`
# puede ser problemático. La solución más explícita y segura es sobreescribir
# los campos que queremos personalizar directamente en nuestra clase.
# Esto reemplaza los campos del `UserCreationForm` padre por los nuestros.
# ==================================================================================
class CustomUserCreationForm(UserCreationForm):
    
    
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Elige un nombre de usuario único',
            'autofocus': True
        })
    )
    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'tu.correo@ejemplo.com'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder' : 'contraseña'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder' : 'confirmar contraseña'
        })
    )

    class Meta:
        model = User
        fields = ['username' , 'email']
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data



# Para el login, usamos AuthenticationForm, el formulario especializado de Django para este propósito.
# Heredamos de él para poder personalizar su apariencia. Esto es más seguro y robusto
# que manejar los campos de usuario y contraseña manualmente.
class LoginForm(AuthenticationForm):
    # Personalizamos los campos para que usen las clases de CSS de Tailwind que ya estás utilizando.
    # Esto se hace sobreescribiendo los campos por defecto.
    username = forms.CharField(label='Ingresa tu email', widget=forms.TextInput(attrs={
        'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        'autofocus': True
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
    }))