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
        "perros": Perro.objects.filter().order_by("nombre")
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
    return render(request, "perros/registrar.html", contexto)

# # VIEWS - CLIENTES

# @login_required
# @user_passes_test(es_veterinario)
# def eliminar(request, dni):
#     cliente = Cliente.objects.get(dni=dni)
#     # cliente.is_active = False BORRADO LÓGICO
#     cliente.delete()
#     return redirect("clientes:listar")

# @login_required
# @user_passes_test(es_veterinario)
# def ver_cliente(request, dni):
#     cliente = Cliente.objects.get(dni=dni)
#     contexto = {
#         "cliente": cliente,
#         "perros_cliente": Perro.objects.filter(cliente=cliente)
#     }
#     return render(request, "clientes/ver-cliente.html", contexto)

