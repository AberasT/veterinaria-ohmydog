from django.forms import Form, IntegerField, CharField,ModelForm, EmailField
from django import forms
from django.contrib.auth import authenticate, login, logout

error_messages = {"required": "Se deben completar todos los campos"}

class IniciarSesionForm(Form):
    email = EmailField(widget=forms.EmailInput, label="Email", required=True, error_messages=error_messages)
    clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.usuario = kwargs.pop('usuario', None)
        super(Form, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        clave = cleaned_data.get('clave')
        if email and clave: 
            if self.usuario is None:
                raise forms.ValidationError("Email y/o contraseña incorrecto/a.")
            elif not self.usuario.is_active:
                raise forms.ValidationError("El usuario ingresado fue eliminado.")
        return email, clave