from django.forms import ModelForm, Form, ModelChoiceField
from .models import Turno
from django.forms.widgets import SelectDateWidget
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}

class SolicitarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha", "perro", "motivo", "detalles"]
        HOY = datetime.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
        }

class ElegirPerroForm(Form):
    
    perro = ModelChoiceField(queryset=None)