from django.shortcuts import render, redirect
from main.tests import es_veterinario, es_cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import  AsignarTurnoForm, ElegirPerroForm, SolicitarTurnoForm, ElegirFechaForm
from .models import Turno
from perros.models import Perro
from correo.SolicitudTurno import SolicitudTurno
from correo.AsignacionTurno import AsignacionTurno
from usuarios.models import Usuario
import datetime

tabla_motivos = {
        'vacunacion general': 'vacunación general',
        'vacunacion antirrabica': 'vacunación antirrábica',
        'castracion': 'castración',
        'consulta': 'consulta general',
        'urgencia': 'consulta de urgencia',
        'desparasitacion': 'desparasitación'
    }

def get_turnos_pendientes(perro):
    turnosPendientes = Turno.objects.filter(perro=perro, hora__isnull=True).order_by("fecha", "hora")
    turnosString = []
    for turno in turnosPendientes:
        turnosString.append(f"Una {tabla_motivos[turno.motivo]} para el día {turno.fecha}.")
    return turnosString

def get_turnos_asignados(perro):
    turnosAsignados = Turno.objects.filter(perro=perro, hora__isnull=False).order_by("fecha", "hora")
    turnosString = []
    for turno in turnosAsignados:
        turnosString.append(f"Una {tabla_motivos[turno.motivo]} para el día {turno.fecha}, hora {turno.hora}.")
    return turnosString

def get_turnos_hoy():
    turnos_hoy = Turno.objects.filter(hora__isnull=False, fecha=datetime.date.today()).order_by("hora")
    turnosString = []
    for turno in turnos_hoy:
        turnosString.append(f"{turno.hora} {tabla_motivos[turno.motivo]} para {turno.perro.nombre} del cliente {turno.perro.responsable.nombre} {turno.perro.responsable.apellido}.")
    return turnosString

def set_opciones_perro(form, user):
    query = Perro.objects.filter(responsable=user)
    choices = []
    for perro in query: choices.append((perro.id, perro.nombre))
    form.fields["perro"].choices = choices

# Create your views here.
@login_required
def index(request):
    turnos = Turno.objects.filter(hora__isnull=False).exclude(fecha=datetime.date.today()).order_by("fecha")
    contexto = {
        "turnos": turnos,
        "turnos_hoy": get_turnos_hoy()
    }
    return render(request, "turnos/index.html", contexto)

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
    form = SolicitarTurnoForm(initial={"fecha":datetime.date.today()})
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
        form = SolicitarTurnoForm(request.POST, perro=perro)
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
def asignar_elegir(request):
    contexto = {
        "perros": Perro.objects.order_by("nombre")
    }
    return render(request, "turnos/asignar_elegir.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def asignar(request, id):
    perro = Perro.objects.get(id=id)
    turnosSolicitados = Turno.objects.filter(perro=perro, hora__isnull=True)
    turno = None
    if turnosSolicitados:
        turno = turnosSolicitados.first()
        form = AsignarTurnoForm(instance=turno)
    else: form = AsignarTurnoForm()
    contexto = {
        "form": form,
        "perro": perro,
        "turno": turno,
        "turnosAsignados": get_turnos_asignados(perro)
    }
    if request.method == "POST":
        if turno is not None: form = AsignarTurnoForm(request.POST, motivo=turno.motivo, perro=perro)
        else: form = AsignarTurnoForm(request.POST, perro=perro)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            motivo = form.cleaned_data["motivo"]
            detalles = form.cleaned_data["detalles"]
            hora = form.cleaned_data["hora"]
            if turno is None:
                turno = Turno(fecha=fecha, perro=perro, hora=hora, motivo=motivo, detalles=detalles)
            else:
                turno.fecha = fecha
                turno.hora = hora
            try:
                turno.save()
                mail = AsignacionTurno(fecha=fecha, hora=hora, perro=perro.nombre, email=perro.responsable.email)
                try:
                    mail.enviar()
                except:
                    return render(request, "main/infomsj.html", {
                    "msj": "No se pudo enviar el correo."
                })
                return render(request, "main/infomsj.html", {
                    "msj": "El turno fue asignado correctamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "No se pudo guardar el turno."
                })
        else:
            contexto["form"] = form
            return render(request, "turnos/asignar.html", contexto)
    return render(request, "turnos/asignar.html", contexto)

@login_required
@user_passes_test(es_cliente)
def mis_turnos(request):
    misTurnos = []
    for turno in Turno.objects.filter(hora__isnull=False).order_by("fecha","hora"):
        if turno.perro.responsable == request.user: misTurnos.append(turno)
    contexto = {
        "misTurnos": misTurnos
    }
    return render(request, "turnos/mis_turnos.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def turnos_fecha(request):
    if request.method == "POST":
        form = ElegirFechaForm(request.POST)
        if form.is_valid():
            turnosFechaAsignados = Turno.objects.filter(hora__isnull=False, fecha=form.cleaned_data["fecha"]).order_by("hora")
            turnosFechaPendientes = Turno.objects.filter(hora__isnull=True, fecha=form.cleaned_data["fecha"])
        eligioFecha = True
    else:
        form = ElegirFechaForm()
        turnosFechaAsignados = []
        turnosFechaPendientes = []
        eligioFecha = False
    contexto = {
        "form": form,
        "turnosFechaAsignados": turnosFechaAsignados,
        "turnosFechaPendientes": turnosFechaPendientes,
        "eligioFecha": eligioFecha
    }
    return render(request, "turnos/turnos_fecha.html", contexto)