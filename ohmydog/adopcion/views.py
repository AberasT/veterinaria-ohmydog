from django.shortcuts import render, redirect
from .forms import publicar_perro_form
from .models import PerroAdopcion
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario
from main.tests import es_veterinario

# Create your views here.

def index(request):
    contexto={
        "publicaciones": PerroAdopcion.objects.all
    }
    return render(request, "adopcion/listar.html", contexto)

@login_required
def publicar_perro(request):
    usuario = request.user
    contexto = {
        "form": publicar_perro_form()
    }
    if request.method == "POST":
        form = publicar_perro_form(request.POST)
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
            publicaciones_usuario = PerroAdopcion.objects.filter(publicador = usuario.id)
            if publicaciones_usuario.filter(nombre=nombre):
                return render(request, "main/infomsj.html",{
                    "msj": "El perro ingresado ya está publicado."
                })
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
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    return render(request, "adopcion/publicar.html", contexto)

@login_required
def marcar_adoptado(request, id):
    perro = PerroAdopcion.objects.get(id=id)
    perro.adoptado = True
    perro.save()
    mis_publicaciones(request)
    return redirect("adopcion:mis_publicaciones")


@login_required
def mis_publicaciones(request):
    usuario = request.user
    publicaciones = PerroAdopcion.objects.filter(publicador=usuario)
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
@user_passes_test(es_veterinario)
def eliminar(request, id):
    publicacion = PerroAdopcion.objects.get(id=id)
    publicacion.delete()
    return redirect("adopcion:index")
