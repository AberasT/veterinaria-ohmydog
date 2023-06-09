from django.shortcuts import render, redirect
from .forms import AgregarVacunaForm
from django.forms import ValidationError
from perros.models import Perro
from .models import Vacuna, Atencion

# Create your views here.

def agregar_vacuna(request, id):
    form = AgregarVacunaForm()
    contexto = {
        "form": form,
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
            
    return render(request, "atenciones/agregar_vacuna.html", contexto)