from django.shortcuts import render, redirect
from .forms import PublicarPerroForm, FiltrarPerroAdopcionForm
from .models import PerroAdopcion
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario
from main.tests import es_veterinario
from datetime import datetime

# Create your views here.

def index(request):
    if request.method == "POST":
        form = FiltrarPerroAdopcionForm(request.POST)
        if form.is_valid():
            publicaciones = PerroAdopcion.objects.filter(activo = True)
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            adoptado = form.cleaned_data["adoptado"]
            if raza != "Sin filtro":
                publicaciones = publicaciones.filter(raza = raza)
            if sexo != "Sin filtro":
                publicaciones = publicaciones.filter(sexo = sexo)
            if adoptado != "Sin filtro":
                publicaciones = publicaciones.filter(adoptado = adoptado)
            publicaciones = publicaciones.order_by("adoptado", "fecha_publicacion")
        filtro = True
    else:
        form = FiltrarPerroAdopcionForm()
        publicaciones = PerroAdopcion.objects.filter(activo=True).order_by("adoptado")
        filtro = False
    contexto = {
        "form": form,
        "publicaciones": publicaciones,
        "filtro": filtro
    }
    return render(request, "adopcion/listar.html", contexto)

@login_required
def publicar_perro(request):
    usuario = request.user
    contexto = {
        "form": PublicarPerroForm()
    }
    if request.method == "POST":
        form = PublicarPerroForm(request.POST, cliente=usuario)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            edad = form.cleaned_data["edad"]
            peso = form.cleaned_data["peso"]
            altura = form.cleaned_data["altura"]
            historial_vacunacion = form.cleaned_data["historial_vacunacion"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            nuevoPerroAdopcion = PerroAdopcion(nombre=nombre, color=color, raza=raza, sexo=sexo,
                                                edad=edad, peso=peso, altura=altura, contacto=contacto,
                                                historial_vacunacion=historial_vacunacion, descripcion=descripcion, publicador=usuario)
            try:
                nuevoPerroAdopcion.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El perro se ha publicado para su adopción exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "adopcion/publicar.html",{"form": form})
    return render(request, "adopcion/publicar.html", contexto)

@login_required
def marcar_adoptado(request, id):
    perro = PerroAdopcion.objects.get(id=id)
    perro.adoptado = True
    perro.fecha_adopcion = datetime.now().date()
    perro.save()
    mis_publicaciones(request)
    return redirect("adopcion:mis_publicaciones")

@login_required
def mis_publicaciones(request):
    publicaciones = PerroAdopcion.objects.filter(publicador=request.user, activo = True).order_by("adoptado")
    contexto = {
        "publicaciones": publicaciones
    }
    return render(request, "adopcion/mis_publicaciones.html", contexto)

@login_required
def info(request, id):
    contexto = {
        "perro": PerroAdopcion.objects.get(id=id)
    }
    return render(request, "adopcion/info.html", contexto)

@login_required
def eliminar(request, id):
    publicacion = PerroAdopcion.objects.get(id=id)
    publicacion.activo = False
    publicacion.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def modificar(request, id):
    usuario = request.user
    publicacion = PerroAdopcion.objects.get(id=id)
    form = PublicarPerroForm(instance=publicacion)
    contexto = {
        "form": form
    }
    if request.method == "POST":
        form = PublicarPerroForm(request.POST, cliente=usuario, id=id)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            edad = form.cleaned_data["edad"]
            peso = form.cleaned_data["peso"]
            altura = form.cleaned_data["altura"]
            historial_vacunacion = form.cleaned_data["historial_vacunacion"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            publicacion.nombre = nombre
            publicacion.color = color
            publicacion.raza = raza
            publicacion.sexo = sexo
            publicacion.edad = edad
            publicacion.peso = peso
            publicacion.altura = altura
            publicacion.historial_vacunacion = historial_vacunacion
            publicacion.descripcion = descripcion
            publicacion.contacto = contacto
            try:
                publicacion.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los datos del perro se han modificado exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "adopcion/modificar.html",{"form": form})
    return render(request, "adopcion/modificar.html", contexto)

@login_required
def filtrar_listado(request, filtro):
    contexto={
        "publicaciones": PerroAdopcion.objects.filter(adoptado = filtro, activo=True) 
    }
    return render(request, "adopcion/listar.html", contexto)

@login_required
def filtrar_mis_publicaciones(request, filtro):
    contexto={
        "publicaciones": PerroAdopcion.objects.filter(adoptado = filtro, activo=True)
    }
    return render(request, "adopcion/mis_publicaciones.html", contexto)