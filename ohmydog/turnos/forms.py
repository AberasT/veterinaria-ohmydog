from django.forms import ModelForm, Form, CharField, ChoiceField
from .models import Turno
from django.forms.widgets import SelectDateWidget, TimeInput
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}

# class SolicitarTurnoForm(ModelForm):
#     class Meta:
#         model = Turno
#         fields = ["fecha", "perro", "motivo", "detalles"]
#         HOY = datetime.today()
#         ANIO = HOY.year
#         widgets = {
#             'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
#         }

class AsignarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha", "hora", "motivo", "detalles"]
        HOY = datetime.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
        }

class ElegirPerroForm(Form):
    
    perro = ChoiceField(choices=(("","")))

# class AsignarTurnoForm(ModelForm):
#     class Meta:
#         model = Turno
#         fields = ["fecha", "hora"]
#         HOY = datetime.today()
#         ANIO = HOY.year
#         widgets = {
#             'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
#             'hora': TimeInput(attrs={'type': 'time'}),
#         }
