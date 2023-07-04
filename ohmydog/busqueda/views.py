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
        "publicaciones": PerroPerdido.objects.all
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
            peso = form.cleaned_data["peso"]
            altura = form.cleaned_data["altura"]
            descripcion = form.cleaned_data["descripcion"]
            contacto = form.cleaned_data["contacto"]
            imagen = form.cleaned_data["imagen"]
            nuevoPerroPerdido = PerroPerdido(nombre=nombre, color=color, raza=raza, sexo=sexo,
                                                edad=edad, peso=peso, altura=altura, contacto=contacto,
                                                imagen=imagen, descripcion=descripcion, publicador=usuario)
            try:
                nuevoPerroPerdido.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El perro perdido se ha publicado exitosamente. Esperamos que sea encontrado pronto."
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
    return render(request)

@login_required
def info(request):
    contexto = {
        "perro": PerroPerdido.objects.get(id=id)
    }
    return render(request, contexto)

@login_required
def eliminar(request):
    contexto = {
        "perro": PerroPerdido.objects.get(id=id)
    }
    return render(request, contexto)