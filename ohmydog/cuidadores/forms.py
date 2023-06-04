from django.forms import Form, CharField, ChoiceField, ModelForm
from django import forms
from .models import Cuidador
from django.forms.widgets import TimeInput
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarCuidadorForm(ModelForm):
    class Meta:
        model = Cuidador
        fields = ["nombre_completo", "edad", "horario_inicial", "horario_final", "experiencia", "contacto"]
        widgets = {
            'horario_inicial': TimeInput(attrs={'type': 'time'}),
            'horario_final' : TimeInput(attrs={'type': 'time'})
        }
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)


    def clean_contacto(self):
        contacto = self.cleaned_data.get("contacto")
        cuidadores = Cuidador.objects.filter(contacto=contacto).exclude(id=self.id)
        if cuidadores:
            raise forms.ValidationError("El contacto ingresado ya se encuentra registrado en el sistema con otro cuidador/paseador.")
        return contacto