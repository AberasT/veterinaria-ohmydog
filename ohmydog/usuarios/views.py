from django.shortcuts import render, redirect
from .forms import RegistrarUsuarioForm, ModificarUsuarioForm
from .models import Usuario
from turnos.models import Turno
from perros.models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario, es_superuser

# VIEWS

@login_required
@user_passes_test(es_veterinario)
def registrar_cliente(request):
    form = RegistrarUsuarioForm()
    contexto = {
        "form": form
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
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else:
            return render(request, "usuarios/registrar-cliente.html", {"form": form})
    return render(request, "usuarios/registrar-cliente.html", contexto)

@login_required
@user_passes_test(es_superuser)
def registrar_veterinario(request):
    form = RegistrarUsuarioForm()
    contexto = {
        "form": form
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
            except:
                print("Exception raised")
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else:
            return render(request, "usuarios/registrar-veterinario.html", {"form": form})
    return render(request, "usuarios/registrar-veterinario.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def index(request):
    contexto = {
        "clientes": Usuario.objects.filter(is_active=True, is_staff=False).order_by("apellido"),
        "inactivos": Usuario.objects.filter(is_active=False, is_staff=False)
    }
    return render(request, "usuarios/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.is_active = False
    usuario.save()
    perros = Perro.objects.filter(responsable=usuario)
    for perro in perros:
        turnosPerro = Turno.objects.filter(is_active=True, asistido=False, perro=perro)
        for turno in turnosPerro:
            turno.is_active = False
            turno.save()
        perro.responsable_activo = False
        perro.save()
    return redirect("usuarios:index")

@login_required
@user_passes_test(es_veterinario)
def ver_cliente(request, id):
    cliente = Usuario.objects.get(id=id)
    contexto = {
        "cliente": cliente,
        "perros_cliente": Perro.objects.filter(responsable=cliente, activo=True)
    }
    return render(request, "usuarios/ver-cliente.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def modificar_cliente(request, id):
    cliente = Usuario.objects.get(id=id)
    form = ModificarUsuarioForm(instance=cliente)
    contexto = {
        "form": form,
        "email": cliente.email
        }
    if request.method == "POST":
        form = ModificarUsuarioForm(request.POST)
        if form.is_valid():
            cliente.dni = form.cleaned_data["dni"]
            cliente.nombre = form.cleaned_data["nombre"]
            cliente.apellido = form.cleaned_data["apellido"]
            cliente.telefono = form.cleaned_data["telefono"]
            #cliente.clave = form.cleaned_data["clave"]
            try:
                cliente.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los cambios se guardaron con éxito"
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else:
            return render(request, "usuarios/modificar-cliente.html", {"form": form, "email": cliente.email})
    return render(request, "usuarios/modificar-cliente.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def historial_clientes(request):
    contexto = {
        "clientes": Usuario.objects.filter(is_active=False, is_staff=False).order_by("apellido")
    }
    return render(request, "usuarios/historial-clientes.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def recuperar_cliente(request, id):
    cliente = Usuario.objects.get(id=id)
    cliente.is_active = True
    cliente.save()
    perros = Perro.objects.filter(responsable=cliente)
    for perro in perros:
        perro.responsable_activo = True
        perro.save()
    contexto = {
        "clientes": Usuario.objects.filter(is_active=False, is_staff=False).order_by("apellido"),
        "recupero": True
    }
    return render(request, "usuarios/historial-clientes.html", contexto)
