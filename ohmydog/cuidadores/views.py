from django.shortcuts import render
from .models import Cuidador

# Create your views here.

def index(request):
    contexto = {
        "cuidadores": Cuidador.objects.all()
    }
    return render(request, "cuidadores/index.html", contexto)