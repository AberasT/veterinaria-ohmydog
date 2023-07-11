from django.forms import ModelForm, forms, ChoiceField
from .models import PerroAdopcion
from django import forms

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
        #publicaciones_no_adoptados_usuario = PerroAdopcion.objects.filter(publicador = self.cliente, adoptado=False)
        nombresPerrosPublicadosLower = [perro.nombre.lower() for perro in PerroAdopcion.objects.filter(publicador=self.cliente, nombre__isnull = False, adoptado = False).exclude(id = self.id)]
        if nombre.lower() in nombresPerrosPublicadosLower:
            raise forms.ValidationError("Ya tienes publicado ese perro en adopción.")
        return nombre

class FiltrarPerroAdopcionForm(forms.Form):
    RAZA_CHOICES = [
        ("Sin filtro", "Sin filtro"),
        ("Desconocida", "NO SE SABE"),
        ("mestizo", "MESTIZO"),
        ("Siberian Husky", "SIBERIAN HUSKY"),
        ("Beagle", "BEAGLE"),
        ("Rottweiler", "ROTTWEILER"),
        ("Bull Terrier", "BULL TERRIER"),
        ("Bulldog Frances", "BULLDOG FRANCES"),
        ("Boxer", "BOXER"),
        ("Dogo Argentino", "DOGO ARGENTINO"),
        ("Gran Danes", "GRAN DANES"),
        ("Labrador", "LABRADOR"),
        ("Galgo", "GALGO"),
        ("Shiba Inu", "SHIBA INU"),
        ("Golden", "GOLDEN"),
        ("Dalmata", "DALMATA"),
        ("Chihuahua", "CHIHUAHUA"),
        ("San Bernardo", "SAN BERNARDO"),
        ("Doberman", "DOBERMAN"),
        ("Pastor Aleman", "PASTOR ALEMAN")
    ]
    TRUE_FALSE_CHOICES = [
        ("Sin filtro", "Sin filtro"),
        (True, 'Si'),
        (False, 'No')
    ]
    SEXO_CHOICES = [
        ("Sin filtro", "Sin filtro"),
        ("macho", "MACHO"),
        ("hembra", "HEMBRA"),
        ("ns", "NS")
    ]
    raza = forms.ChoiceField(choices=RAZA_CHOICES, initial="Sin Filtro", required=False)
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, initial="Sin Filtro", required=False)
    adoptado = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, initial="Sin Filtro", required=False)