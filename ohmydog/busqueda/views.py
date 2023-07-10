from django.shortcuts import render, redirect
from .forms import PublicarPerroPerdidoForm, FiltrarPerroPerdidoForm
from .models import PerroPerdido
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario
from main.tests import es_veterinario
from datetime import datetime
from .forms import FiltrarPerroPerdidoForm

#create your views
def listar(request):
    if request.method == "POST":
        form = FiltrarPerroPerdidoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["zona"] == "Sin filtro": publicaciones = PerroPerdido.objects.filter(activo=True).order_by("-perdido")
            else: publicaciones = PerroPerdido.objects.filter(activo=True, zona=form.cleaned_data["zona"]).order_by("fecha_publicacion")
        filtro = True
    else:
        form = FiltrarPerroPerdidoForm()
        publicaciones = PerroPerdido.objects.filter(activo=True).order_by("-perdido"),
        filtro = False
    contexto = {
        "form": form,
        "publicaciones": publicaciones,
        "filtro": filtro
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
            zona = form.cleaned_data["zona"]
            direccion = form.cleaned_data["direccion"]
            es_propio = form.cleaned_data["es_propio"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            imagen = request.FILES.get('imagen')
            nuevoPerroPerdido = PerroPerdido(nombre=nombre, color=color, raza=raza, sexo=sexo, es_propio = es_propio, zona=zona, direccion=direccion,
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
    publicaciones = PerroPerdido.objects.filter(publicador=request.user, activo=True).order_by("-perdido")
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
def eliminar(request, id):
    perro = PerroPerdido.objects.get(id = id)
    perro.activo = False
    perro.save()
    return redirect(request.META.get('HTTP_REFERER')
)

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
            imagen = request.FILES.get('imagen_nueva')
            publicacion.nombre = form.cleaned_data["nombre"]
            publicacion.color = form.cleaned_data["color"]
            publicacion.raza = form.cleaned_data["raza"]
            publicacion.sexo = form.cleaned_data["sexo"]
            publicacion.edad = form.cleaned_data["edad"]
            publicacion.zona = form.cleaned_data["zona"]
            publicacion.direccion = form.cleaned_data["direccion"]
            publicacion.es_propio = form.cleaned_data["es_propio"]
            publicacion.descripcion = form.cleaned_data["descripcion"]
            publicacion.contacto = form.cleaned_data["contacto"]
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

@login_required
def filtrar(request, filtro):
    contexto={
        "publicaciones": PerroPerdido.objects.filter(perdido = filtro, activo=True)
    }
    return render(request, "busqueda/index.html", contexto)

@login_required
def filtrar_mis_publicaciones(request, filtro):
    contexto={
        "publicaciones": PerroPerdido.objects.filter(perdido = filtro, activo=True)
    }
    return render(request, "busqueda/mis_publicaciones.html", contexto)