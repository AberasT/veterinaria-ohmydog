from django.shortcuts import render, redirect
from usuarios.models import Usuario
from .forms import RegistrarPerroForm
from .models import Perro
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario
from atenciones.models import Vacuna, Atencion
from turnos.models import Turno

# VIEWS

@login_required
@user_passes_test(es_veterinario)
def index(request):
    contexto = {
        "perros": Perro.objects.filter(activo=True, responsable_activo=True).order_by("nombre"),
        "inactivos": Perro.objects.filter(activo=False),
        "inactivos_responsable": Perro.objects.filter(responsable_activo=False)
    }
    return render(request, "perros/listar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request, id):
    cliente = Usuario.objects.get(id=id)
    form = RegistrarPerroForm()
    contexto = {
        "cliente": cliente,
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
            castrado = form.cleaned_data["castrado"]
            nuevoPerro = Perro(nombre=nombre, color=color, raza=raza, sexo=sexo, fecha_nacimiento=fecha_nacimiento, peso=peso, responsable=cliente, castrado=castrado)
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
    perro.activo = False
    perro.save()
    turnosPerro = Turno.objects.filter(is_active=True, asistido=False, perro=perro)
    for turno in turnosPerro:
        turno.is_active = False
        turno.save()
    return redirect("perros:index")

@login_required
@user_passes_test(es_veterinario)
def ver_perro(request, id):
    perro = Perro.objects.get(id=id)
    atenciones = Atencion.objects.filter(perro=perro).order_by("-fecha")
    vacunas = Vacuna.objects.filter(perro=perro).order_by("-fecha")
    contexto = {
        "perro": perro,
        "atenciones": atenciones,
        "vacunas": vacunas
    }
    return render(request, "perros/ver-perro.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def modificar(request, id):
    perro = Perro.objects.get(id=id)
    cliente = perro.responsable
    form = RegistrarPerroForm(instance=perro)
    contexto = {
        "perro": perro,
        "form": form
    }
    if request.method == "POST":
        form = RegistrarPerroForm(request.POST, cliente=cliente, id=id)
        if form.is_valid():
            perro.nombre = form.cleaned_data["nombre"]
            perro.color = form.cleaned_data["color"]
            perro.raza = form.cleaned_data["raza"]
            perro.sexo = form.cleaned_data["sexo"]
            perro.castrado = form.cleaned_data["castrado"]
            perro.fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            perro.peso = form.cleaned_data["peso"]
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

@login_required
@user_passes_test(es_veterinario)
def historial_perros(request):
    contexto = {
        "perros": Perro.objects.filter(activo=False, responsable_activo=True).order_by("nombre"),
        "perros_responsable": Perro.objects.filter( responsable_activo=False).order_by("nombre")
    }
    return render(request, "perros/historial-perros.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def recuperar_perro(request, id):
    perro = Perro.objects.get(id=id)
    perro.activo = True
    perro.save()
    contexto = {
        "perros": Perro.objects.filter(activo=False).order_by("nombre"),
        "recupero": True,
    }
    return render(request, "perros/historial-perros.html", contexto)

