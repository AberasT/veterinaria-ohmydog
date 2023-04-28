from django.shortcuts import render
from .forms import CreateUserForm

# Create your views here.
def registrar(request):
    contexto = {
        "form": CreateUserForm()
        }
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "clientes/registrar.html", contexto)