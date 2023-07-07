from django.shortcuts import render, redirect
from .forms import PublicarPerroPerdidoForm
from .models import PerroPerdido
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario
from main.tests import es_veterinario
from datetime import datetime

#create your views
def listar(request):
    contexto={
        "publicaciones": PerroPerdido.objects.order_by("-perdido")
    }
    return render(request, "busqueda/index.html", contexto)

@login_required
def publicar_perro(request):
    usuario = request.user
    contexto = {
        "form": PublicarPerroPerdidoForm()
    }
    if request.method == "POST":
        form = PublicarPerroPerdidoForm(request.POST, request.FILES, cliente=usuario)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            edad = form.cleaned_data["edad"]
            es_propio = form.cleaned_data["es_propio"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            imagen = request.FILES.get('imagen')
            nuevoPerroPerdido = PerroPerdido(nombre=nombre, color=color, raza=raza, sexo=sexo, es_propio = es_propio,
                                                edad=edad, contacto=contacto, imagen=imagen, descripcion=descripcion, publicador=usuario)
            try:
                nuevoPerroPerdido.save()
                if es_propio:
                    return render(request, "main/infomsj.html", {
                        "msj": "El perro perdido se ha publicado exitosamente. Esperamos que sea encontrado pronto."
                    })
                else:
                    return render(request, "main/infomsj.html", {
                        "msj": "El perro perdido se ha publicado exitosamente. Esperamos que su dueño aparezca pronto."
                    })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "busqueda/publicar.html",{"form": form})
    return render(request, "busqueda/publicar.html", contexto)


@login_required
def mis_publicaciones(request):
    publicaciones = PerroPerdido.objects.filter(publicador=request.user).order_by("-perdido")
    contexto = {
        "publicaciones": publicaciones
    }
    return render(request, "busqueda/mis_publicaciones.html", contexto)

@login_required
def marcar_encontrado(request, id):
    perro = PerroPerdido.objects.get(id=id)
    perro.perdido = False
    perro.fecha_encontrado = datetime.now().date()
    perro.save()
    mis_publicaciones(request)
    return redirect("busqueda:mis_publicaciones")

@login_required
def info(request, id):
    contexto = {
        "perro": PerroPerdido.objects.get(id=id)
    }
    return render(request, "busqueda/info.html", contexto)

@login_required
def eliminar(request):
    contexto = {
        "perro": PerroPerdido.objects.get(id=id)
    }
    return render(request, contexto)

@login_required
def modificar(request, id):
    usuario = request.user
    publicacion = PerroPerdido.objects.get(id=id)
    form = PublicarPerroPerdidoForm(instance = publicacion)
    contexto = {
        "form": form,
        "imagen_cargada": publicacion.imagen
    }
    if request.method == "POST":
        form = PublicarPerroPerdidoForm(request.POST, request.FILES, cliente=usuario, id=id)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            color = form.cleaned_data["color"]
            raza = form.cleaned_data["raza"]
            sexo = form.cleaned_data["sexo"]
            edad = form.cleaned_data["edad"]
            es_propio = form.cleaned_data["es_propio"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            imagen = request.FILES.get('imagen_nueva')
            publicacion.nombre = nombre
            publicacion.color = color
            publicacion.raza = raza
            publicacion.sexo = sexo
            publicacion.edad = edad
            publicacion.es_propio = es_propio
            publicacion.descripcion = descripcion
            publicacion.contacto = contacto
            if imagen:
                publicacion.imagen = imagen
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
            return render(request, "busqueda/modificar.html",{"form": form, "imagen_cargada": publicacion.imagen})
    return render(request, "busqueda/modificar.html", contexto)