from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import RegistrarUsuarioForm
from .models import Usuario
from perros.models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario, es_superuser

# VIEWS

@login_required
@user_passes_test(es_veterinario)
def registrar_cliente(request):
    contexto = {
        "form": RegistrarUsuarioForm()
        }
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            clave = form.cleaned_data["clave"]
            nuevoUsuario = Usuario(dni=dni, nombre=nombre, apellido=apellido, email=email, telefono=telefono, clave=clave)
            nuevoUsuario.set_password(clave)
            try:
                nuevoUsuario.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El cliente se ha registrado exitosamente"
                })
            except IntegrityError:
                print("Exception raised")
                return render(request, "main/infomsj.html",{
                    "msj": "El email ingresado ya se encuentra registrado en el sistema."
                })
        else:
            return render(request, "main/infomsj.html",{
                    "msj": "El email ingresado ya se encuentra registrado en el sistema."
                })
    return render(request, "usuarios/registrar-cliente.html", contexto)

@login_required
@user_passes_test(es_superuser)
def registrar_veterinario(request):
    contexto = {
        "form": RegistrarUsuarioForm()
        }
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            clave = form.cleaned_data["clave"]
            nuevoUsuario = Usuario(dni=dni, nombre=nombre, apellido=apellido, email=email, is_staff=True, telefono=telefono, clave=clave)
            nuevoUsuario.set_password(clave)
            try:
                nuevoUsuario.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El veterinario se ha registrado exitosamente"
                })
            except IntegrityError:
                print("Exception raised")
                return render(request, "main/infomsj.html",{
                    "msj": "El email ingresado ya se encuentra registrado en el sistema."
                })
    return render(request, "usuarios/registrar-veterinario.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def index(request):
    contexto = {
        "clientes": Usuario.objects.filter(is_active=True, is_staff=False).order_by("apellido")
    }
    return render(request, "usuarios/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    usuario = Usuario.objects.get(id=id)
    # cliente.is_active = False BORRADO LÓGICO
    usuario.delete()
    return redirect("usuarios:index")

@login_required
@user_passes_test(es_veterinario)
def ver_cliente(request, id):
    cliente = Usuario.objects.get(id=id)
    contexto = {
        "cliente": cliente,
        "perros_cliente": Perro.objects.filter(responsable=cliente)
    }
    return render(request, "usuarios/ver-cliente.html", contexto)
