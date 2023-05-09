from django.forms import ModelForm
from .models import PerroAdopcion

error_messages = {"required": "Se deben completar todos los campos"}

class publicar_perro_form(ModelForm):
    class Meta:
        model = PerroAdopcion
        fields = ["nombre", "color", "raza", "sexo", "edad", "peso",
         "altura", "contacto", "historial_vacunacion", "descripcion"]