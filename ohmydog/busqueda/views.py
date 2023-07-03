from django.shortcuts import render, redirect
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
    return render(request, "busqueda/listar.html", contexto)

@login_required
def publicar_perro(request):
    contexto={
    }
    return render(request)

@login_required
def mis_publicaciones(request):
    return render(request)

