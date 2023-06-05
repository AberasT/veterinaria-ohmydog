from django.forms import ModelForm
from django import forms
from .models import Perro
from django.forms.widgets import SelectDateWidget, CheckboxInput
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarPerroForm(ModelForm):
    class Meta:
        HOY = datetime.now().year
        model = Perro
        fields = ["nombre", "raza", "color", "sexo", "castrado", "fecha_nacimiento", "peso"]
        widgets = {
            'fecha_nacimiento': SelectDateWidget(years=range(HOY-20, HOY+1) , attrs={'type': 'date'}),
            "castrado": CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop('cliente', None)
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        perros_cliente = Perro.objects.filter(responsable = self.cliente)
        if perros_cliente.filter(nombre=nombre).exclude(id=self.id):
            raise forms.ValidationError(f"{self.cliente.nombre} {self.cliente.apellido} ya tiene registrado ese perro.")
        return nombre