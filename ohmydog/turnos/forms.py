from django.forms import ModelForm, Form, ChoiceField, ValidationError, DateField
from .models import Turno
import datetime
from atenciones.models import Vacuna
from django.forms.widgets import SelectDateWidget, TimeInput

error_messages = {"required": "Se deben completar todos los campos"}

def puede_solicitar_turno(perro, motivo):
    turnosPendientes = Turno.objects.filter(perro=perro, hora__isnull=True)
    while True:
        if any(turnoPendiente.motivo == motivo for turnoPendiente in turnosPendientes): return False
        else: return True

def puede_solicitar_vacuna(perro, motivo, fechaSolicitud):
    ultimaVacunaDada = Vacuna.objects.filter(perro=perro, vacuna=motivo).order_by("fecha").last()
    if ultimaVacunaDada and fechaSolicitud is not None:
        diff = fechaSolicitud - ultimaVacunaDada.fecha
        print(diff.days)
        if diff.days < 120: return False
    return True

class SolicitarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha", "motivo", "detalles"]
        HOY = datetime.date.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.perro = kwargs.pop('perro', None)
        self.hora = kwargs.pop('hora', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < datetime.date.today():
            raise ValidationError(f"La fecha elegida no puede ser anterior a la actual.")
        return fecha
    
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo == "castración" and self.perro.castrado:
            raise ValidationError(f"{self.perro.nombre} se encuentra castrado/a acorde a nuestros registros.")
        elif motivo in ("vacunación general", "vacunación antirrábica"):
            if not puede_solicitar_vacuna(self.perro, motivo, self.cleaned_data.get("fecha")):
                raise ValidationError(f"{self.perro.nombre} tiene una vacuna registrada del mismo tipo hace menos de 120 días.")
        if not puede_solicitar_turno(self.perro, motivo):
            raise ValidationError(f"{self.perro.nombre} ya tiene un turno pendiente con el motivo de {motivo}.")
        return motivo
    
class AsignarTurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ["fecha", "hora", "motivo", "detalles"]
        HOY = datetime.date.today()
        ANIO = HOY.year
        widgets = {
            'fecha': SelectDateWidget(years=[ANIO], attrs={'type': 'date'}),
            'hora': TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.perro = kwargs.pop('perro', None)
        self.motivo = kwargs.pop('motivo', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < datetime.date.today():
            raise ValidationError(f"La fecha elegida no puede ser anterior a la actual.")
        return fecha
    
    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if hora is None:
            raise ValidationError(f"Debe elegir un horario.")
        return hora
    
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo == "":
            raise ValidationError(f"Debe elegir un motivo.")
        return motivo
    
class ElegirPerroForm(Form):
    perro = ChoiceField(choices=(("","")))

class ElegirFechaForm(Form):
    fecha = DateField(initial=datetime.date.today(), widget=SelectDateWidget(attrs={'type': 'date'}))

