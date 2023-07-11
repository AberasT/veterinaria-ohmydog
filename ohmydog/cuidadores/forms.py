from django.forms import Form, CharField, ModelForm, EmailField, TextInput
from .models import Cuidador, Solicitud
from django.forms.widgets import TimeInput
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class RegistrarCuidadorForm(ModelForm):
    class Meta:
        model = Cuidador
        fields = ["nombre_completo", "edad", "disponibilidad", "experiencia", "contacto"]
    widgets ={
        "disponibilidad": TextInput()
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
    
class SolicitarContactoForm(Form):
    email = EmailField(widget=forms.EmailInput, label="Email", required=True, error_messages=error_messages)
    nombre = CharField(max_length=20, required=True)
    apellido = CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', None)
        super(Form, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        cuidador = Cuidador.objects.get(id=self.id)
        solicitudes = Solicitud.objects.filter(email=email, cuidador=cuidador)
        if solicitudes:
            raise forms.ValidationError("Ya solicitó el contacto del cuidador con ese email")
        return email