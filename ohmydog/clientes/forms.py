from django.forms import Form, IntegerField, CharField,ModelForm
from .models import Cliente
from django import forms

class RegistrarClienteForm(Form):
    dni = IntegerField(label="DNI", required=True)
    nombre = CharField(label="Nombre", max_length=30, required=True)
    apellido = CharField(label="Apellido", max_length=30, required=True)
    email = CharField(widget=forms.EmailInput, label="Email", required=True)
    clave = forms.CharField(widget=forms.PasswordInput, required=True)