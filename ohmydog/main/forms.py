from django.forms import Form, IntegerField, CharField,ModelForm, EmailField
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class IniciarSesionForm(Form):
    email = EmailField(widget=forms.EmailInput, label="Email", required=True, error_messages=error_messages)
    clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)

class CambiarClaveForm(Form):
    clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)
    repetir_clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)