from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import RegistrarClienteForm, RegistrarPerroForm
from .models import Cliente
from django.contrib.auth.decorators import login_required, user_passes_test

# TESTS
def es_veterinario(user):
    return user.is_staff


# VIEWS
@login_required
@user_passes_test(es_veterinario)
def index(request):
    contexto = {
        "form": RegistrarClienteForm()
        }
    return render(request, "clientes/index.html", contexto)


# VIEWS - CLIENTES
@login_required
@user_passes_test(es_veterinario)
def registrar_cliente(request):
    contexto = {
        "form": RegistrarClienteForm()
        }
    
    if request.method == "POST":
        form = RegistrarClienteForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            clave = form.cleaned_data["clave"]
            nuevoCliente = Cliente(dni=dni, nombre=nombre, apellido=apellido, email=email, telefono=telefono, clave=clave)
            nuevoCliente.set_password(clave)
            try:
                nuevoCliente.save()
                return render(request, "clientes/exito.html", contexto)
            except IntegrityError:
                print("Exception raised")
                return render(request, "clientes/error.html",{
                    "error": "El DNI ingresado ya se encuentra registrado en el sistema."
                })
        else: 
            print("Form is not valid")
            return render(request, "clientes/registrar_cliente.html", {"form": form})
    return render(request, "clientes/registrar_cliente.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def listar(request):
    contexto = {
        "clientes": Cliente.objects.filter(is_active=True, is_staff=False).order_by("apellido")
    }
    return render(request, "clientes/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def eliminar(request, dni):
    cliente = Cliente.objects.get(dni=dni)
    # cliente.is_active = False BORRADO LÓGICO
    cliente.delete()
    return redirect("clientes:listar")

@login_required
@user_passes_test(es_veterinario)
def ver_cliente(request, dni):
    contexto = {
        "cliente": Cliente.objects.get(dni=dni)
    }
    return render(request, "clientes/ver-cliente.html", contexto)


# VIEWS - PERROS

@login_required
@user_passes_test(es_veterinario)
def registrar_perro(request, dni):
    contexto = {
        "form": RegistrarPerroForm()
        }
    
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            clave = form.cleaned_data["clave"]
            nuevoCliente = Cliente(dni=dni, nombre=nombre, apellido=apellido, email=email, telefono=telefono, clave=clave)
            nuevoCliente.set_password(clave)
            try:
                nuevoCliente.save()
                return render(request, "clientes/exito.html", contexto)
            except IntegrityError:
                print("Exception raised")
                return render(request, "clientes/error.html",{
                    "error": "El DNI ingresado ya se encuentra registrado en el sistema."
                })
        else: 
            print("Form is not valid")
            return render(request, "clientes/registrar_cliente.html", {"form": form})
    return render(request, "clientes/registrar_cliente.html", contexto)
