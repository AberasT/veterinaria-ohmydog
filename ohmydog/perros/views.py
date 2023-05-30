from django.shortcuts import render, redirect
from usuarios.models import Usuario
from .forms import RegistrarPerroForm
from .models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario
from datetime import datetime

# VIEWS

@login_required
@user_passes_test(es_veterinario)
def index(request):
    contexto = {
        "perros": Perro.objects.order_by("nombre")
    }
    return render(request, "perros/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request, id):
    cliente = Usuario.objects.get(id=id)
    form = RegistrarPerroForm()
    contexto = {
        "form": form
        }
    
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST, cliente=cliente)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            peso = form.cleaned_data["peso"]
            nuevoPerro = Perro(nombre=nombre, color=color, raza=raza, sexo=sexo, fecha_nacimiento=fecha_nacimiento, peso=peso, responsable=cliente)
            try:
                nuevoPerro.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El perro se ha registrado exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "perros/registrar.html", {"form": form})
    return render(request, "perros/registrar.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    perro = Perro.objects.get(id=id)
    perro.delete()
    return redirect("perros:index")

@login_required
@user_passes_test(es_veterinario)
def ver_perro(request, id):
    perro = Perro.objects.get(id=id)
    contexto = {
        "perro": perro
    }
    return render(request, "perros/ver-perro.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def modificar(request, id):
    perro = Perro.objects.get(id=id)
    print(perro.fecha_nacimiento)
    cliente = perro.responsable
    form = RegistrarPerroForm(instance=perro)
    contexto = {
        "form": form
    }
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST, cliente=cliente, id=id)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            peso = form.cleaned_data["peso"]
            perro.nombre = nombre
            perro.color = color
            perro.raza = raza
            perro.sexo = sexo
            perro.fecha_nacimiento = fecha_nacimiento
            perro.peso = peso
            try:
                perro.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los cambios se guardaron con éxito."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "perros/modificar.html", {"form": form})
    return render(request, "perros/modificar.html", contexto)


