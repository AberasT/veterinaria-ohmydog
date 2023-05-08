from django.shortcuts import render, redirect
from django.db import IntegrityError
from clientes.models import Cliente
from .forms import RegistrarPerroForm
from .models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test

# TESTS
def es_veterinario(user):
    return user.is_staff

# VIEWS
@login_required
@user_passes_test(es_veterinario)
def index(request):
    return render(request, "perros/index.html")

@login_required
@user_passes_test(es_veterinario)
def listar(request):
    contexto = {
        "perros": Perro.objects.order_by("nombre")
    }
    return render(request, "perros/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request, dni):
    contexto = {
        "form": RegistrarPerroForm()
        }
    
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            peso = form.cleaned_data["peso"]
            cliente = Cliente.objects.get(dni=dni)
            nuevoPerro = Perro(nombre=nombre, color=color, raza=raza, sexo=sexo, fecha_nacimiento=fecha_nacimiento, peso=peso, cliente=cliente)
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
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    return render(request, "perros/registrar.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    perro = Perro.objects.get(id=id)
    perro.delete()
    return redirect("perros:listar")

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
    form = RegistrarPerroForm(instance=perro)
    contexto = {
        "perro": perro,
        "form": form
    }
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST)
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
                    "msj": "Los datos del perro se han modificado exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    return render(request, "perros/modificar.html", contexto)


