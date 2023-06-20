from django.shortcuts import render, redirect
from .models import Cuidador, Solicitud
from .forms import RegistrarCuidadorForm, SolicitarContactoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario
from correo.SolicitudContacto import SolicitudContacto
from correo.AprobacionContacto import AprobacionContacto
from correo.RechazoContacto import RechazoContacto
from usuarios.models import Usuario
from django.db import IntegrityError
import datetime

# Create your views here.

def index(request):
    cuidadores_solicitados = []
    cuidadores_aprobados = []
    cuidadores_sin_aprobar = []
    if request.user.id:
        solicitudes_usuario = Solicitud.objects.filter(cliente=request.user)
        for solicitud in solicitudes_usuario:
            if solicitud.aprobada:
                cuidadores_aprobados.append(solicitud.cuidador)
            else:    
                cuidadores_solicitados.append(solicitud.cuidador)
        solicitudes = Solicitud.objects.filter(aprobada=False)
        for solicitud in solicitudes:
            cuidadores_sin_aprobar.append(solicitud.cuidador)
    contexto = {
        "cuidadores": Cuidador.objects.all(),
        "cuidadores_solicitados": cuidadores_solicitados,
        "cuidadores_aprobados": cuidadores_aprobados,
        "solicito": False,
        "cuidadores_sin_aprobar": cuidadores_sin_aprobar
    }
    return render(request, "cuidadores/index.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def registrar(request):
    form = RegistrarCuidadorForm()
    contexto = {
        "form": form
        }
    
    if request.method == "POST":
        form = RegistrarCuidadorForm(request.POST)
        if form.is_valid():
            nombre_completo = form.cleaned_data["nombre_completo"]
            edad = form.cleaned_data["edad"]
            horario_inicial = form.cleaned_data["horario_inicial"]
            horario_final = form.cleaned_data["horario_final"]
            experiencia = form.cleaned_data["experiencia"]
            contacto = form.cleaned_data["contacto"]
            nuevoCuidador = Cuidador(nombre_completo=nombre_completo, edad=edad, horario_inicial=horario_inicial, horario_final=horario_final, experiencia=experiencia, contacto=contacto)
            try:
                nuevoCuidador.save()
                return render(request, "main/infomsj.html", {
                    "msj": "El cuidador/paseador se publicó exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "cuidadores/registrar.html",{"form":form})
    return render(request, "cuidadores/registrar.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def eliminar(request, id):
    cuidador = Cuidador.objects.get(id=id)
    cuidador.delete()
    return redirect("cuidadores:index")


@login_required
@user_passes_test(es_veterinario)
def modificar(request, id):
    publicacion = Cuidador.objects.get(id=id)
    form = RegistrarCuidadorForm(instance=publicacion)
    contexto = {
        "form": form
    }
    if request.method == "POST":
        form = RegistrarCuidadorForm(request.POST, id=id)
        if form.is_valid():
            nombre_completo = form.cleaned_data["nombre_completo"]
            edad = form.cleaned_data["edad"]
            horario_inicial = form.cleaned_data["horario_inicial"]
            horario_final = form.cleaned_data["horario_final"]
            experiencia = form.cleaned_data["experiencia"]
            contacto = form.cleaned_data["contacto"]
            publicacion.nombre_completo = nombre_completo
            publicacion.edad = edad
            publicacion.horario_inicial = horario_inicial
            publicacion.horario_final = horario_final
            publicacion.experiencia = experiencia
            publicacion.contacto = contacto
            try:
                publicacion.save()
                return render(request, "main/infomsj.html", {
                    "msj": "Los datos del cuidador/paseador se han modificado exitosamente."
                })
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "cuidadores/modificar.html",{"form": form})
    return render(request, "cuidadores/modificar.html", contexto)

@login_required
def solicitar(request, id):
    cuidador = Cuidador.objects.get(id=id)
    cliente = request.user
    nuevaSolicitud = Solicitud(cliente=cliente, cuidador=cuidador, nombre=cliente.nombre, apellido=cliente.apellido, email=cliente.email )
    try:
        nuevaSolicitud.save()
        solicitudes_usuario = Solicitud.objects.filter(cliente=request.user)
        cuidadores_solicitados = []
        cuidadores_aprobados = []
        for solicitud in solicitudes_usuario:
            if solicitud.aprobada:
                cuidadores_aprobados.append(solicitud.cuidador)
            else:    
                cuidadores_solicitados.append(solicitud.cuidador)
        contexto = {
            "cuidadores": Cuidador.objects.all(),
            "cuidadores_solicitados": cuidadores_solicitados,
            "cuidadores_aprobados": cuidadores_aprobados,
            "solicito": True
        }
        mail= SolicitudContacto(cliente.email, cuidador.nombre_completo)
        try:
            mail.enviar()
        except:
            return render(request, "main/infomsj.html", {
                "msj": "Ha ocurrido un error."
        })
        return render(request, "cuidadores/index.html", contexto)
    except:
        return render(request, "main/infomsj.html",{
            "msj": "Ha ocurrido un error."
        })
    
@login_required
@user_passes_test(es_veterinario)
def listar_solicitudes(request, id):
    cuidador = Cuidador.objects.get(id=id)
    solicitudes = Solicitud.objects.filter(cuidador=cuidador, aprobada=False)
    contexto = {
        "cuidador": cuidador,
        "solicitudes": solicitudes
    }
    return render(request, "cuidadores/listar_solicitudes.html", contexto)

@login_required
@user_passes_test(es_veterinario)
def aceptar_solicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)
    solicitud.aprobada = True
    try:
        solicitud.save()
        cuidador = solicitud.cuidador
        solicitudes = Solicitud.objects.filter(cuidador=cuidador, aprobada=False)
        contexto = {
            "cuidador": cuidador,
            "solicitudes": solicitudes,
            "aceptada": True
        }
        mail = AprobacionContacto(solicitud.email, solicitud.cuidador.contacto)
        mail.enviar()
        return render(request, "cuidadores/listar_solicitudes.html", contexto)
    except:
        return render(request, "main/infomsj.html",{
            "msj": "Ha ocurrido un error."
        })

@login_required
@user_passes_test(es_veterinario)
def rechazar_solicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)
    cuidador = solicitud.cuidador
    mail = RechazoContacto(solicitud.email)
    mail.enviar()
    solicitud.delete()
    solicitudes = Solicitud.objects.filter(cuidador=cuidador, aprobada=False)
    contexto = {
        "cuidador": cuidador,
        "solicitudes": solicitudes,
        "rechazada": True
    }
    
    return render(request, "cuidadores/listar_solicitudes.html", contexto)

def solicitar_visitante(request, id):
    cuidador = Cuidador.objects.get(id=id)
    form = SolicitarContactoForm()
    contexto = {
        "form": form
    }
    if request.method == "POST":
        form = SolicitarContactoForm(request.POST, id=id)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            email = form.cleaned_data["email"]
            nuevaSolicitud = Solicitud(cuidador=cuidador, nombre=nombre, apellido=apellido, email=email )
            try:
                nuevaSolicitud.save()
                contexto["cuidadores"] = Cuidador.objects.all()
                contexto["solicito"] = True
                return render(request, "cuidadores/index.html", contexto)
            except:
                return render(request, "main/infomsj.html",{
                    "msj": "Ha ocurrido un error."
                })
        else: 
            return render(request, "cuidadores/solicitar_visitante.html",{"form": form})
    return render(request, "cuidadores/solicitar_visitante.html", contexto)