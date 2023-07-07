from django.forms import ModelForm, forms
from .models import PerroPerdido
from django.forms.widgets import RadioSelect
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class PublicarPerroPerdidoForm(ModelForm):
    class Meta:
        model = PerroPerdido
        fields = ["nombre", "color", "raza", "sexo", "es_propio", "edad",
         "peso", "contacto", "altura", "descripcion"]
        
        TRUE_FALSE_CHOICES = [
        (True, 'Si'),
        (False, 'No')
        ]
        widgets = {
            "es_propio": RadioSelect(choices=TRUE_FALSE_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop('cliente', None)
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        nombre = self.cleaned_data.get('nombre')
        es_propio = self.cleaned_data.get('es_propio')
        publicaciones_perdidos_usuario = PerroPerdido.objects.filter(publicador = self.cliente, perdido=True)
        if not es_propio:
            None
        elif not nombre:
            raise forms.ValidationError("Tiene que ingresar el nombre al que responde su perro perdido.")
        elif publicaciones_perdidos_usuario.filter(nombre=nombre).exclude(id = self.id):
            raise forms.ValidationError(f"{self.cliente.nombre} {self.cliente.apellido} ya tiene publicado ese perro perdido.")
        return self.cleaned_data