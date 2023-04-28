from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "main/index.html", {
    })

# def login(request):
#     contexto = {
#         "form": ()
#         }
#     return render(request, "clientes/registrar.html", contexto)