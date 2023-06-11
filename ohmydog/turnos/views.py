from django.shortcuts import render, redirect
from django.forms import ValidationError
from main.tests import es_veterinario, es_cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import  AsignarTurnoForm, ElegirPerroForm
from .models import Turno
from perros.models import Perro
from correo.SolicitudTurno import SolicitudTurno
from correo.AsignacionTurno import AsignacionTurno
from usuarios.models import Usuario

def get_turnos_pendientes(perro):
    turnosPendientes = Turno.objects.filter(perro=perro, hora__isnull=True)
    turnosString = []
    tabla_motivos = {
        'vacunacion general': 'vacunación general',
        'vacunacion antirrabica': 'vacunación antirrábica',
        'castracion': 'castración',
        'consulta': 'consulta general',
        'urgencia': 'consulta de urgencia',
        'desparasitacion': 'desparasitación'
    }
    for turno in turnosPendientes:
        turnosString.append(f"Una {tabla_motivos[turno.motivo]} para el día {turno.fecha}.")
    return turnosString

def set_opciones_perro(form, user):
    query = Perro.objects.filter(responsable=user)
    choices = []
    for perro in query: choices.append((perro.id, perro.nombre))
    form.fields["perro"].choices = choices

# Create your views here.
@login_required
def index(request):
    return render(request, "turnos/index.html")

@login_required
@user_passes_test(es_cliente)
def elegir_perro(request):
    form = ElegirPerroForm()
    set_opciones_perro(form, request.user)
    contexto = {
        "form": form
    }
    if request.method == "POST": return redirect("turnos:solicitar", id=request.POST["perro"])
    return render(request, "turnos/elegir_perro.html", contexto)

@login_required
@user_passes_test(es_cliente)
def solicitar(request, id):
    form = AsignarTurnoForm()
    contexto = {}
    try:
        perro = Perro.objects.get(id=id)
        if perro.responsable == request.user:
            contexto = {
            "perro": perro,
            "form": form,
            "turnosPendientes": get_turnos_pendientes(perro)
        }
    except:
        perro = None

    if request.method == "POST":
        form = AsignarTurnoForm(request.POST, perro=perro)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            motivo = form.cleaned_data["motivo"]
            detalles = form.cleaned_data["detalles"]
            nuevoTurno = Turno(fecha=fecha, perro=perro, motivo=motivo, detalles=detalles)
            try:
                nuevoTurno.save()
                mail = SolicitudTurno(fecha=fecha, perro=perro.nombre, motivo=motivo, detalles=detalles, email=request.user.email)
                try:
                    mail.enviar()
                    return render(request, "main/infomsj.html", {
                        "msj": "El turno está a la espera de confirmación. Cualquier novedad será informada vía email"
                    })
                except:
                    return render(request, "main/infomsj.html", {
                    "msj": "No se pudo enviar el correo."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "No se pudo guardar el turno."
                })
        else:
            contexto["form"] = form
            return render(request, "turnos/solicitar.html", contexto)
    return render(request, "turnos/solicitar.html", contexto)


@login_required
@user_passes_test(es_veterinario)
def asignar(request, id):
    perro = Perro.objects.get(id=id)
    if Turno.objects.filter(perro=perro, hora__isnull=True):
        turno = Turno.objects.filter(perro=perro).last()
        form = AsignarTurnoForm(instance=turno)
    else: form = AsignarTurnoForm()
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
                turno = Turno(fecha=fecha, perro=perro, motivo=motivo, detalles=detalles)
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