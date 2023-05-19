from django.shortcuts import render
from main.tests import es_veterinario, es_cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SolicitarTurnoForm
from .models import Turno
from correo.SolicitudTurno import SolicitudTurno

# Create your views here.
@login_required
def index(request):
    return render(request, "turnos/index.html")

@login_required
@user_passes_test(es_cliente)
def solicitar(request):
    form = SolicitarTurnoForm()
    contexto = {
        "form": SolicitarTurnoForm()
    }

    if request.method == "POST":
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            perro = form.cleaned_data["perro"]
            motivo = form.cleaned_data["motivo"]
            detalles = form.cleaned_data["detalles"]
            cliente = request.user
            nuevoTurno = Turno(fecha=fecha, perro=perro, motivo=motivo, detalles=detalles, cliente=cliente)
            try:
                nuevoTurno.save()
                mail = SolicitudTurno(fecha=fecha, perro=perro, motivo=motivo, detalles=detalles, email=cliente.email)
                try:
                    mail.enviar()
                except Exception as ex:
                    return render(request, "main/infomsj.html", {
                    "msj": type(ex).__name__
                })
                return render(request, "main/infomsj.html", {
                    "msj": "El turno está a la espera de confirmación. Cualquier novedad será informada vía email"
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    
    return render(request, "turnos/solicitar.html", contexto)