from django.forms import ModelForm, forms
from .models import PerroAdopcion

error_messages = {"required": "Se deben completar todos los campos"}

class PublicarPerroForm(ModelForm):
    class Meta:
        model = PerroAdopcion
        fields = ["nombre", "color", "raza", "sexo", "edad", "peso",
         "altura", "contacto", "historial_vacunacion", "descripcion"]
        
    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop('cliente', None)
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        publicaciones_no_adoptados_usuario = PerroAdopcion.objects.filter(publicador = self.cliente, adoptado=False)
        if publicaciones_no_adoptados_usuario.filter(nombre=nombre).exclude(id = self.id):
            raise forms.ValidationError(f"{self.cliente.nombre} {self.cliente.apellido} ya tiene publicado ese perro en adopción.")
        return nombre