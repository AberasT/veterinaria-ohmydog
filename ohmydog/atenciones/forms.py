from .models import Vacuna, Atencion
from django.forms import ModelForm, SelectDateWidget

class AgregarVacunaForm(ModelForm):
    class Meta:
        model = Vacuna
        fields = ["fecha", "vacuna", "dosis"]
        widgets = {
            'fecha': SelectDateWidget(attrs={'type': 'date'}),
        }

class AgregarAtencionForm(ModelForm):
    class Meta:
        model = Atencion
        fields = ["fecha", "motivo", "descripcion"]
        widgets = {
            'fecha': SelectDateWidget(attrs={'type': 'date'}),
        }