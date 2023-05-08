from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import RegistrarClienteForm
from .models import Cliente
from perros.models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test

# TESTS
def es_veterinario(user):
    return user.is_staff


# VIEWS

@login_required
@user_passes_test(es_veterinario)
def index(request):
    return render(request, "clientes/index.html")

@login_required
@user_passes_test(es_veterinario)
def registrar(request):
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
                return render(request, "main/infomsj.html", {
                    "msj": "El cliente se ha registrado exitosamente"
                })
            except IntegrityError:
                print("Exception raised")
                return render(request, "main/infomsj.html",{
                    "msj": "El DNI ingresado ya se encuentra registrado en el sistema."
                })
    return render(request, "clientes/registrar.html", contexto)

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
    cliente = Cliente.objects.get(dni=dni)
    contexto = {
        "cliente": cliente,
        "perros_cliente": Perro.objects.filter(cliente=cliente)
    }
    return render(request, "clientes/ver-cliente.html", contexto)
