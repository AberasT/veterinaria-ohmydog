from django.shortcuts import render
from main.tests import es_veterinario, es_cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import  AsignarTurnoForm
from .models import Turno
from perros.models import Perro
from correo.SolicitudTurno import SolicitudTurno
from correo.AsignacionTurno import AsignacionTurno
from usuarios.models import Usuario

# Create your views here.
@login_required
def index(request):
    return render(request, "turnos/index.html")

@login_required
@user_passes_test(es_cliente)
def elegir_perro(request):
    form = ElegirPerroForm()
    form.fields["perro"].queryset = Perro.objects.filter(responsable=request.user)
    contexto = {
        "form": form
    }
    return render(request, "turnos/elegir_perro.html", contexto)


@login_required
@user_passes_test(es_cliente)
def solicitar(request):
    form = AsignarTurnoForm()
    contexto = {
        "form": form
    }

    if request.method == "POST":
        form = AsignarTurnoForm(request.POST)
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
                except:
                    return render(request, "main/infomsj.html", {
                    "msj": "Ha ocurrido un error."
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


@login_required
@user_passes_test(es_veterinario)
def asignar(request, id):
    cliente = Usuario.objects.get(id=id)
    if Turno.objects.filter(cliente=cliente, hora__isnull=True):
        turno = Turno.objects.filter(cliente=cliente).last()
        form = AsignarTurnoForm(instance=turno)
    else:
        form = AsignarTurnoForm()
    
    contexto = {
        "form": form
    }
    if request.method == "POST":
        form = AsignarTurnoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            perro = form.cleaned_data["perro"]
            motivo = form.cleaned_data["motivo"]
            detalles = form.cleaned_data["detalles"]
            hora = form.cleaned_data["hora"]
            cliente = Usuario.objects.get(id=id)
            if not "turno" in locals():
                turno = Turno(fecha=fecha, perro=perro, motivo=motivo, detalles=detalles, cliente=cliente)
            else:
                turno.fecha = fecha
                turno.hora = hora
            try:
                turno.save()
                mail = AsignacionTurno(fecha=fecha, hora=hora, email=cliente.email)
                try:
                    mail.enviar()
                except:
                    return render(request, "main/infomsj.html", {
                    "msj": "Ha ocurrido un error."
                })
                return render(request, "main/infomsj.html", {
                    "msj": "El turno fue asignado correctamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "main/infomsj.html",{
                "msj": "Ha ocurrido un error."
            })
    
    return render(request, "turnos/asignar.html", contexto)