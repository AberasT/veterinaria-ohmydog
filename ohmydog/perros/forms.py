from django.forms import Form, CharField, ChoiceField
from django import forms
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarPerroForm(Form):
    SEXO_CHOICES = [("H", "Hembra"), ("M", "Macho"), ("-", "NS")]
    years = [x for x in range(2000,datetime.now().year+1)]

    nombre = CharField(label="Nombre", max_length=20, required=True, error_messages=error_messages)
    color = CharField(label="Color", max_length=20, required=True, error_messages=error_messages)
    raza = CharField(label="Raza", required=True, error_messages=error_messages)
    sexo = ChoiceField(label="Sexo", choices=SEXO_CHOICES, required=True, error_messages=error_messages)
    fecha_nacimiento = forms.DateField(widget=forms.SelectDateWidget(years=years), required=True, label="Fecha de nacimiento", error_messages=error_messages)
    peso = CharField(label="Peso", required=True, error_messages=error_messages)
