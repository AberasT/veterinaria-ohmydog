from django.forms import Form, IntegerField, CharField, ModelForm
from .models import Perro
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarClienteForm(Form):
    dni = IntegerField(label="DNI", required=True, error_messages=error_messages)
    nombre = CharField(label="Nombre", max_length=30, required=True, error_messages=error_messages)
    apellido = CharField(label="Apellido", max_length=30, required=True, error_messages=error_messages)
    email = CharField(widget=forms.EmailInput, label="Email", required=True, error_messages=error_messages)
    telefono = forms.CharField(required=True, error_messages=error_messages)
    clave = forms.CharField(widget=forms.PasswordInput, required=True, error_messages=error_messages)

class RegistrarPerroForm(Form):
    SEXO_FIELDS = ["Hembra", "Macho", "-"]

    nombre = CharField(label="Nombre", max_length=20, required=True, error_messages=error_messages)
    color = CharField(label="Color", max_length=20, required=True, error_messages=error_messages)
    raza = CharField(label="Raza", required=True, error_messages=error_messages)
    sexo = forms.ComboField(label="Sexo", fields=SEXO_FIELDS, error_messages=error_messages)
    fecha_nacimiento = forms.DateField(widget=forms.SelectDateWidget, label="Fecha de nacimiento", error_messages=error_messages)
    peso = CharField(label="Peso", required=True, error_messages=error_messages)
