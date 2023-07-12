from django.shortcuts import render, redirect
from .forms import AgregarVacunaForm, AgregarAtencionForm
from perros.models import Perro
from .models import Vacuna, Atencion
from turnos.models import Turno
import datetime
from main.tests import es_veterinario
from django.contrib.auth.decorators import login_required, user_passes_test


MOTIVO_CHOICES = (
    ('castración', 'Castración'),
    ('consulta', 'Consulta general'),
    ('desparasitación', 'Desparasitación')
)
# Create your views here.

@login_required
@user_passes_test(es_veterinario)
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

@login_required
@user_passes_test(es_veterinario)
def agregar_atencion(request, id):
    form = AgregarAtencionForm(initial={"fecha": datetime.date.today()})
    form.fields["motivo"].choices = MOTIVO_CHOICES
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

@login_required
@user_passes_test(es_veterinario)
def modificar_atencion(request, id):
    atencion = Atencion.objects.get(id=id)
    form = AgregarAtencionForm(instance=atencion)
    form.fields["motivo"].choices = MOTIVO_CHOICES
    contexto = {
        "perro": atencion.perro,
        "form": form
    }
    if request.method == "POST":
        form = AgregarAtencionForm(request.POST)
        if form.is_valid():
            atencion.fecha = form.cleaned_data["fecha"]
            atencion.motivo = form.cleaned_data["motivo"]
            atencion.descripcion = form.cleaned_data["descripcion"]
            if atencion.motivo == "castración":
                perro = Perro.objects.get(id=atencion.perro.id)
                perro.castrado = True
                perro.save()
            try:
                atencion.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los cambios se guardaron con éxito.",
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "atenciones/modificar_atencion.html", {"perro": atencion.perro, "form": form})
    return render(request, "atenciones/modificar_atencion.html", {"perro": atencion.perro, "form": form })

@login_required
@user_passes_test(es_veterinario)
def modificar_vacuna(request, id):
    vacuna = Vacuna.objects.get(id=id)
    form = AgregarVacunaForm(instance=vacuna)
    contexto = {
        "perro": vacuna.perro,
        "form": form
    }
    if request.method == "POST":
        form = AgregarVacunaForm(request.POST)
        if form.is_valid():
            vacuna.fecha = form.cleaned_data["fecha"]
            vacuna.vacuna = form.cleaned_data["vacuna"]
            vacuna.dosis = form.cleaned_data["dosis"]
            try:
                vacuna.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los cambios se guardaron con éxito."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "atenciones/modificar_vacuna.html", {"perro": vacuna.perro, "form": form})
    return render(request, "atenciones/modificar_vacuna.html", { "perro": vacuna.perro, "form": form })

@login_required
@user_passes_test(es_veterinario)
def eliminar_atencion(request, id):
    atencion = Atencion.objects.get(id=id)
    atencion.delete()
    return redirect("perros:info", id=atencion.perro.id)

@login_required
@user_passes_test(es_veterinario)
def eliminar_vacuna(request, id):
    vacuna = Vacuna.objects.get(id=id)
    vacuna.delete()
    return redirect("perros:info", id=vacuna.perro.id)