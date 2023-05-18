from django.shortcuts import render
from .models import Cuidador
from .forms import RegistrarCuidadorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario

# Create your views here.

def index(request):
    contexto = {
        "cuidadores": Cuidador.objects.all()
    }
    return render(request, "cuidadores/index.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request):
    contexto = {
        "form": RegistrarCuidadorForm()
        }
    
    if request.method == "POST":
        form = RegistrarCuidadorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            edad = form.cleaned_data["edad"]
            for cuidador in Cuidador.objects.all():
                if cuidador.nombre == nombre and cuidador.edad == edad :
                    return render(request, "main/infomsj.html",{
                        "msj": f"El cuidador/paseador {nombre} ya se encuentra publicado y no puede volver a publicarse."
                    })
            horario_inicio = form.cleaned_data["horario_inicio"]
            horario_fin = form.cleaned_data["horario_fin"]
            experiencia = form.cleaned_data["experiencia"]
            contacto = form.cleaned_data["contacto"]
            nuevoCuidador = Cuidador(nombre=nombre, edad=edad, horario_inicio=horario_inicio, horario_fin=horario_fin, experiencia=experiencia, contacto=contacto)
            try:
                nuevoCuidador.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El cuidador/paseador se ha registrado exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    return render(request, "cuidadores/registrar.html", contexto)