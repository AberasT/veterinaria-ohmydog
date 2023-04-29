from django.forms import Form, IntegerField, CharField,ModelForm
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class IniciarSesionForm(Form):
    dni = IntegerField(label="DNI", required=True, error_messages=error_messages)
    clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)