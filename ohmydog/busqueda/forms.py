from django.forms import ModelForm, forms
from .models import PerroPerdido
from django.forms.widgets import RadioSelect, ChoiceWidget
from django import forms

error_messages = {"required": "Se deben completar todos los campos"}

class PublicarPerroPerdidoForm(ModelForm):
    class Meta:
        model = PerroPerdido
        fields = ["nombre", "color", "raza", "sexo", "es_propio", "edad",
         "contacto", "descripcion"]
        
        TRUE_FALSE_CHOICES = [
        (True, 'Si'),
        (False, 'No')
        ]
        widgets = {
            "es_propio": RadioSelect(choices=TRUE_FALSE_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop('cliente', None)
        self.id = kwargs.pop('id', None)
        super(ModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        nombre = self.cleaned_data.get('nombre')
        es_propio = self.cleaned_data.get('es_propio')
        nombresPerrosPublicadosLower = [perro.nombre.lower() for perro in PerroPerdido.objects.filter(publicador=self.cliente, nombre__isnull = False, perdido= True).exclude(id = self.id)]
        #publicaciones_perdidos_usuario = PerroPerdido.objects.filter(publicador = self.cliente, perdido=True)
        if not es_propio:
            None
        elif not nombre:
            raise forms.ValidationError("Tiene que ingresar el nombre al que responde su perro perdido.")
        elif nombre.lower() in nombresPerrosPublicadosLower:
            raise forms.ValidationError("Ya tienes publicado ese perro perdido.")
        return self.cleaned_data

class FiltrarPerroPerdidoForm(forms.Form):
    fields = ["raza", "sexo", "perdido"]
    raza = forms.CharField(max_length=20, required = False, widget=ChoiceWidget)
    sexo = forms.CharField(max_length=20, required = False, widget=ChoiceWidget)
    perdido = forms.CharField(max_length=20, required = False, widget=ChoiceWidget)
    SEXO_CHOICES = [
    ("macho", "MACHO"),
    ("hembra", "HEMBRA"),
    ("ns", "NS")
    ]
    RAZA_CHOICES = [
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
        ("Shiba Inu", "AKITA INU"),
        ("Golden", "GOLDEN"),
        ("Dalmata", "DALMATA"),
        ("Chihuahua", "CHIHUAHUA"),
        ("San Bernardo", "SAN BERNARDO"),
        ("Doberman", "DOBERMAN"),
        ("Pastor Aleman", "PASTOR ALEMAN")
    ]
    TRUE_FALSE_CHOICES = [
    (True, 'Si'),
    (False, 'No')
    ]
    widgets = {
        "encontrado": ChoiceWidget(choices=TRUE_FALSE_CHOICES),
        "raza": ChoiceWidget(choices=RAZA_CHOICES),
        "sexo": ChoiceWidget(choices=SEXO_CHOICES)
    }