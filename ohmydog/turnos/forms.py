from django.forms import ModelForm
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
        fields = ["fecha","hora", "perro", "motivo", "detalles"]
        HOY = datetime.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
            'hora': TimeInput(attrs={'type': 'time'})
        }

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