from django.shortcuts import render, redirect
from .forms import IniciarSesionForm, CambiarClaveForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import ValidationError
from usuarios.models import Usuario

# TESTS
def usuario_no_autenticado(user):
    return not user.is_authenticated

# VIEWS
def index(request):
    return render(request, "main/index.html", {
    })

@user_passes_test(usuario_no_autenticado)
def login_view(request):
    contexto = {
        "form": IniciarSesionForm()
        }
    
    if request.method == "POST":
        email = request.POST["email"]
        clave = request.POST["clave"]
        usuario = authenticate(request, username=email, password=clave)
        if usuario is not None:
            login(request, usuario)
            if usuario.primer_login:
                return redirect("main:cambiar_clave")
            return redirect("main:index")
        else:
            messages.info(request, "Email y/o contraseña incorrecto/a")

    return render(request, "main/login.html", contexto)

@login_required
def logout_view(request):
    logout(request)
    return redirect("main:index")

@login_required
def cambiar_clave(request):
    form = CambiarClaveForm()
    contexto = {
        "form": form
    }

    if request.method == "POST":
        if form.is_valid():
            clave1 = form.cleaned_data["clave"]
            clave2 = form.cleaned_data["repetir_clave"]
            if clave1 != clave2:
                return render(request, "main/infomsj.html", {
                    "msj": "Las claves deben coincidir."
                })
            else:
                usuario = Usuario.objects.get(email=request.user.email)
                usuario.clave = clave1
                usuario.save()
                usuario.primer_login = False
                return render(request, "main/infomsj.html", {
                    "msj": "La clave se ha actualizado."
                })
        else:
            return render(request, "main/infomsj.html", {
                    "msj": "Error."
                })
    return render(request, "main/cambiar_clave.html", contexto)