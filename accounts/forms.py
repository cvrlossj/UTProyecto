from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(  
        label="Run",  
        widget=forms.TextInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Ingresa tu RUN',
            'required': 'required',
            'autofocus': 'autofocus',
            'autocomplete': 'on',
            'oninput': 'validateRut(this)', 
            'maxlength': '8',
            'pattern': '[0-9]*'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'Ingresa tu Contraseña',
            'required': 'required',
            'autofocus': 'autofocus',
            'autocomplete': 'on',
        })
    )