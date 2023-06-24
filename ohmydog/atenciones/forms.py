from .models import Vacuna, Atencion
from django.forms import ModelForm, SelectDateWidget, ValidationError
import datetime

class AgregarVacunaForm(ModelForm):
    class Meta:
        model = Vacuna
        fields = ["fecha", "vacuna", "dosis"]
        widgets = {
            'fecha': SelectDateWidget(attrs={'type': 'date'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha > datetime.date.today():
            raise ValidationError(f"La fecha elegida debe ser igual o anterior a la actual.")
        return fecha

class AgregarAtencionForm(ModelForm):
    class Meta:
        model = Atencion
        fields = ["fecha", "motivo", "descripcion"]
        widgets = {
            'fecha': SelectDateWidget(attrs={'type': 'date'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha > datetime.date.today():
            raise ValidationError(f"La fecha elegida debe ser igual o anterior a la actual.")
        return fecha