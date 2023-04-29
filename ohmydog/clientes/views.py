from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import RegistrarClienteForm
from .models import Cliente

# Create your views here.
def index(request):
    contexto = {
        "form": RegistrarClienteForm()
        }
    return render(request, "clientes/index.html", contexto)

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
                return render(request, "clientes/exito.html", contexto)
            except IntegrityError:
                print("Exception raised")
                return render(request, "clientes/error.html",{
                    "error": "El DNI ingresado ya se encuentra registrado en el sistema."
                })
        else: 
            print("Form is not valid")
            return render(request, "clientes/registrar.html", {"form": form})
    return render(request, "clientes/registrar.html", contexto)

def listar(request):
    contexto = {
        "clientes": Cliente.objects.order_by("apellido"),
    }
    return render(request, "clientes/listar.html", contexto)