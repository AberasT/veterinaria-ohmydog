from django.shortcuts import render, redirect
from .models import Cuidador
from .forms import RegistrarCuidadorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario
from django.db import IntegrityError
import datetime

# Create your views here.

def index(request):
    contexto = {
        "cuidadores": Cuidador.objects.all()
    }
    return render(request, "cuidadores/index.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request):
    form = RegistrarCuidadorForm()
    contexto = {
        "form": form
        }
    
    if request.method == "POST":
        form = RegistrarCuidadorForm(request.POST)
        if form.is_valid():
            nombre_completo = form.cleaned_data["nombre_completo"]
            edad = form.cleaned_data["edad"]
            horario_inicial = form.cleaned_data["horario_inicial"]
            horario_final = form.cleaned_data["horario_final"]
            experiencia = form.cleaned_data["experiencia"]
            contacto = form.cleaned_data["contacto"]
            nuevoCuidador = Cuidador(nombre_completo=nombre_completo, edad=edad, horario_inicial=horario_inicial, horario_final=horario_final, experiencia=experiencia, contacto=contacto)
            try:
                nuevoCuidador.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El cuidador/paseador se publicó exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "cuidadores/registrar.html",{"form":form})
    return render(request, "cuidadores/registrar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    cuidador = Cuidador.objects.get(id=id)
    cuidador.delete()
    return redirect("cuidadores:index")