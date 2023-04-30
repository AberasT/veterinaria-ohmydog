from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import RegistrarClienteForm, RegistrarPerroForm
from .models import Cliente, Perro
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
                return render(request, "clientes/exito.html", {
                    "msj": "El cliente se ha registrado exitosamente"
                })
            except IntegrityError:
                print("Exception raised")
                return render(request, "clientes/error.html",{
                    "error": "El DNI ingresado ya se encuentra registrado en el sistema."
                })
        else: 
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
                return render(request, "clientes/exito.html", {
                    "msg": "El perro se ha registrado exitosamente"
                })
            except:
                print("Exception raised")
                return render(request, "clientes/error.html",{
                    "error": "Ha ocurrido un error."
                })
        else: 
            return render(request, "clientes/registrar_perro.html", {"form": form})
    return render(request, "clientes/registrar_perro.html", contexto)
