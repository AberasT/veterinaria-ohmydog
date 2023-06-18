from django.shortcuts import render, redirect
from .forms import AgregarVacunaForm, AgregarAtencionForm
from perros.models import Perro
from .models import Vacuna, Atencion
import datetime

# Create your views here.

def agregar_vacuna(request, id):
    form = AgregarVacunaForm(initial={"fecha": datetime.date.today()})
    contexto = {
        "form": form,
        "perro": Perro.objects.get(id=id)
    }
    if request.method == "POST":
        form = AgregarVacunaForm(request.POST)
        if form.is_valid():
            nuevaVacuna = Vacuna(perro=Perro.objects.get(id=id),
                                 vacuna=form.cleaned_data["vacuna"],
                                 fecha=form.cleaned_data["fecha"],
                                 dosis=form.cleaned_data["dosis"])
            try:
                nuevaVacuna.save()
                return render(request, "main/infomsj.html", {
                    "msj": "La vacuna se agregó exitosamente."
                })
            except:
                return render(request, "main/infomsj", {
                    "msj": "No se pudo guardar la vacuna."
                })       
    return render(request, "atenciones/agregar_atencion.html", contexto)

def agregar_atencion(request, id):
    form = AgregarAtencionForm(initial={"fecha": datetime.date.today()})
    perro = Perro.objects.get(id=id)
    contexto = {
        "form": form,
        "perro": perro
    }
    if request.method == "POST":
        form = AgregarAtencionForm(request.POST)
        if form.is_valid():
            nuevaAtencion = Atencion(perro=Perro.objects.get(id=id),
                                motivo=form.cleaned_data["motivo"],
                                fecha=form.cleaned_data["fecha"],
                                descripcion=form.cleaned_data["descripcion"])
            if form.cleaned_data["motivo"] == "castración":
                perro.castrado = True
                perro.save()
            try:
                nuevaAtencion.save()
                return render(request, "main/infomsj.html", {
                    "msj": "La atención se agregó exitosamente."
                })
            except:
                return render(request, "main/infomsj", {
                    "msj": "No se pudo guardar la atención."
                })       
    return render(request, "atenciones/agregar_atencion.html", contexto)