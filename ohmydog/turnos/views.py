from django.shortcuts import render, redirect
from main.tests import es_veterinario, es_cliente
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import  AsignarTurnoForm, ElegirPerroForm, SolicitarTurnoForm, ElegirFechaForm
from atenciones.forms import AgregarAtencionForm, AgregarVacunaForm
from .models import Turno
from perros.models import Perro
from correo.SolicitudTurno import SolicitudTurno
from correo.AsignacionTurno import AsignacionTurno
from atenciones.models import Atencion, Vacuna
import datetime

def get_turnos_pendientes(perro):
    turnosPendientes = Turno.objects.filter(is_active=True, perro=perro, hora__isnull=True).order_by("fecha", "hora")
    turnosString = []
    for turno in turnosPendientes:
        turnosString.append(f"Una {turno.motivo} para el día {turno.fecha}.")
    return turnosString

def get_turnos_asignados(perro):
    turnosAsignados = Turno.objects.filter(is_active=True, asistido=False, perro=perro, hora__isnull=False).order_by("fecha", "hora")
    turnosString = []
    for turno in turnosAsignados:
        turnosString.append(f"Una {turno.motivo} para el día {turno.fecha}, hora {turno.hora}.")
    return turnosString

def get_turnos_hoy():
    turnos_hoy = Turno.objects.filter(is_active=True, asistido=False, hora__isnull=False, fecha=datetime.date.today()).order_by("hora")
    turnosString = []
    for turno in turnos_hoy:
        if turno.perro.activo and turno.perro.responsable_activo:
            turnosString.append(f"{turno.hora} {turno.motivo} para {turno.perro.nombre} del cliente {turno.perro.responsable.nombre} {turno.perro.responsable.apellido}.")
    return turnosString

def set_opciones_perro(form, user):
    query = Perro.objects.filter(responsable=user, activo=True)
    choices = []
    for perro in query: choices.append((perro.id, perro.nombre))
    form.fields["perro"].choices = choices

# Create your views here.
@login_required
def index(request):
    contexto = {
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
        "perros": Perro.objects.filter(activo=True, responsable_activo=True).order_by("nombre")
    }
    return render(request, "turnos/asignar_elegir.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def asignar(request, id):
    perro = Perro.objects.get(id=id)
    turnosSolicitados = Turno.objects.filter(is_active=True, asistido=False, perro=perro, hora__isnull=True)
    turno = None
    if turnosSolicitados:
        turno = turnosSolicitados.first()
        form = AsignarTurnoForm(instance=turno)
    else: form = AsignarTurnoForm(initial={"fecha":datetime.date.today()})
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
    for turno in Turno.objects.filter(is_active=True, asistido=False, hora__isnull=False).order_by("fecha","hora"):
        if turno.perro.responsable == request.user and turno.perro.activo: 
            misTurnos.append(turno)
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
            turnosFechaAsignados = Turno.objects.filter(is_active=True, hora__isnull=False, fecha=form.cleaned_data["fecha"]).order_by("hora")
            turnosFechaPendientes = Turno.objects.filter(is_active=True, hora__isnull=True, fecha=form.cleaned_data["fecha"]).order_by("fecha")
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

@login_required
@user_passes_test(es_veterinario)
def confirmar_asistencia(request):
    turnosPasados = Turno.objects.filter(is_active=True, asistido=False, fecha__lte=datetime.date.today()).order_by("fecha", "hora")
    contexto = {
        "turnosPasados": turnosPasados
    }
    return render(request, "turnos/confirmar_asistencia.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def turno_asistio(request, id):
    turnoAsistido = Turno.objects.get(id=id)
    if request.method == "POST":
        if turnoAsistido.motivo in ("vacunación general", "vacunación antirrábica"):
            form = AgregarVacunaForm(request.POST)
            if form.is_valid():
                nuevaVacuna = Vacuna(perro=turnoAsistido.perro,
                                    vacuna=form.cleaned_data["vacuna"],
                                    fecha=form.cleaned_data["fecha"],
                                    dosis=form.cleaned_data["dosis"])
                try:
                    nuevaVacuna.save()
                    turnoAsistido.asistido = True
                    turnoAsistido.save()
                    return render(request, "main/infomsj.html", {
                        "msj": "La vacuna se agregó exitosamente."
                    })
                except:
                    return render(request, "main/infomsj", {
                        "msj": "No se pudo guardar la vacuna."
                    })
        else:
            form = AgregarAtencionForm(request.POST)
            if form.is_valid():
                nuevaAtencion = Atencion(perro=turnoAsistido.perro,
                                    motivo=form.cleaned_data["motivo"],
                                    fecha=form.cleaned_data["fecha"],
                                    descripcion=form.cleaned_data["descripcion"])
                if form.cleaned_data["motivo"] == "castración":
                    turnoAsistido.perro.castrado = True
                    turnoAsistido.perro.save()
                try:
                    nuevaAtencion.save()
                    turnoAsistido.asistido = True
                    turnoAsistido.save()
                    return render(request, "main/infomsj.html", {
                        "msj": "La atención se agregó exitosamente."
                    })
                except:
                    return render(request, "main/infomsj", {
                        "msj": "No se pudo guardar la atención."
                    })       
    else:
        if turnoAsistido.motivo in ("vacunación general", "vacunación antirrábica"):
            form = AgregarVacunaForm(initial={
                "fecha": turnoAsistido.fecha,
                "perro": turnoAsistido.perro,
                "vacuna": turnoAsistido.motivo,
                "dosis": turnoAsistido.detalles
                })
        else: 
            form = AgregarAtencionForm(initial={
                "fecha": turnoAsistido.fecha,
                "perro": turnoAsistido.perro,
                "motivo": turnoAsistido.motivo,
                "descripcion": turnoAsistido.detalles
                })
    contexto = {
        "form": form,
        "turno": turnoAsistido,
    }
    return render(request, "turnos/asistencia.html", contexto)

def turno_no_asistio(request, id):
    turnoNoAsistido = Turno.objects.get(id=id)
    turnoNoAsistido.is_active = False
    turnoNoAsistido.save()
    return redirect("turnos:confirmar_asistencia")