from django.shortcuts import render, redirect
from .forms import IniciarSesionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "main/index.html", {
    })

def loginView(request):
    contexto = {
        "form": IniciarSesionForm()
        }
    
    if request.method == "POST":
        dni = request.POST["dni"]
        clave = request.POST["clave"]
        usuario = authenticate(request, username=dni, password=clave)
        if usuario is not None:
            login(request, usuario)
            return redirect("main:index")
        else:
            messages.info(request, "DNI y/o contraseña incorrecto/a")

    return render(request, "main/login.html", contexto)

def logoutView(request):
    logout(request)
    return redirect("main:index")
