from django.shortcuts import render, redirect
from .forms import IniciarSesionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# TESTS
def usuario_no_autenticado(user):
    return not user.is_authenticated

# VIEWS
def index(request):
    return render(request, "main/index.html", {})

@user_passes_test(usuario_no_autenticado)
def login_view(request):
    form = IniciarSesionForm()
    contexto = {
        "form": form
        }
    
    if request.method == "POST":
        email = request.POST["email"]
        clave = request.POST["clave"]
        usuario = authenticate(request, username=email, password=clave)
        form = IniciarSesionForm(request.POST, usuario=usuario)
        if form.is_valid():
            if usuario is not None:
                login(request, usuario)
                return redirect("main:index")
        else:
            return render(request, "main/login.html", {"form":form})
    return render(request, "main/login.html", contexto)

@login_required
def logout_view(request):
    logout(request)
    return redirect("main:index")
