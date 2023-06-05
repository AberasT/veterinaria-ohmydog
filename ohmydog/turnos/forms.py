from django.forms import ModelForm, Form, CharField, ChoiceField, ValidationError
from .models import Turno
from django.forms.widgets import SelectDateWidget, TimeInput
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}

def puede_solicitar_turno(perro, motivo):
    turnosPendientes = Turno.objects.filter(perro=perro, hora__isnull=True)
    while True:
        if any(turnoPendiente.motivo == motivo for turnoPendiente in turnosPendientes): return False
        else: return True

class AsignarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha", "hora", "motivo", "detalles"]
        HOY = datetime.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.perro = kwargs.pop('perro', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if not puede_solicitar_turno(self.perro, motivo):
            raise ValidationError(f"{self.perro.nombre} ya tiene un turno pendiente con el motivo de {motivo}.")
        return motivo

class ElegirPerroForm(Form):    
    perro = ChoiceField(choices=(("","")))

