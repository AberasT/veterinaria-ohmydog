from django.forms import ModelForm, Form, ChoiceField, ValidationError
from .models import Turno
import datetime
from atenciones.models import Vacuna
from django.forms.widgets import SelectDateWidget
from datetime import datetime

error_messages = {"required": "Se deben completar todos los campos"}
tabla_motivos = {
        'vacunacion general': 'vacunación general',
        'vacunacion antirrabica': 'vacunación antirrábica',
        'castracion': 'castración',
        'consulta': 'consulta general',
        'urgencia': 'consulta de urgencia',
        'desparasitacion': 'desparasitación'
    }

def puede_solicitar_turno(perro, motivo):
    turnosPendientes = Turno.objects.filter(perro=perro, hora__isnull=True)
    while True:
        if any(turnoPendiente.motivo == motivo for turnoPendiente in turnosPendientes): return False
        else: return True

def puede_solicitar_vacuna(perro, motivo):
    ultimaVacunaDada = Vacuna.objects.filter(perro=perro, vacuna=motivo).order_by("fecha").first()
    if ultimaVacunaDada:
        print(ultimaVacunaDada.fecha)
        hoy = datetime.now()
        fechaUltimaVacuna = datetime.date(ultimaVacunaDada.fecha)
        diff = hoy - fechaUltimaVacuna
        if diff.days < 120: return False
    return True

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
        if motivo == "castracion" and self.perro.castrado:
            raise ValidationError(f"{self.perro.nombre} se encuentra castrado/a acorde a nuestros registros.")
        elif motivo == "vacunacion general" or motivo == "vacunacion antirrabica":
            if not puede_solicitar_vacuna(self.perro, motivo):
                raise ValidationError(f"{self.perro.nombre} tiene una vacuna registrada del mismo tipo hace menos de 120 días.")
        elif not puede_solicitar_turno(self.perro, motivo):
            raise ValidationError(f"{self.perro.nombre} ya tiene un turno pendiente con el motivo de {tabla_motivos[motivo]}.")
        return motivo

class ElegirPerroForm(Form):
    perro = ChoiceField(choices=(("","")))

