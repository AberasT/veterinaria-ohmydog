from django.shortcuts import render, redirect
from .models import Cuidador, Solicitud
from .forms import RegistrarCuidadorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from main.tests import es_veterinario
from correo.SolicitudContacto import SolicitudContacto
from correo.AprobacionContacto import AprobacionContacto
from usuarios.models import Usuario
from django.db import IntegrityError
import datetime

# Create your views here.

def index(request):
    solicitudes_usuario = Solicitud.objects.filter(cliente=request.user)
    cuidadores_solicitados = []
    cuidadores_aprobados = []
    for solicitud in solicitudes_usuario:
        if solicitud.aprobada:
            cuidadores_aprobados.append(solicitud.cuidador)
        else:    
            cuidadores_solicitados.append(solicitud.cuidador)
    solicitudes = Solicitud.objects.filter(aprobada=False)
    cuidadores_sin_aprobar = []
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
    nuevaSolicitud = Solicitud(cliente=cliente, cuidador=cuidador)
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
        mail = AprobacionContacto(solicitud.cliente.email, solicitud.cuidador.contacto)
        mail.enviar()
        return render(request, "main/infomsj.html", {
            "msj": "El contacto del cuidador/paseador fue enviado al cliente."
        })
    except:
        return render(request, "main/infomsj.html",{
            "msj": "Ha ocurrido un error."
        })

@login_required
@user_passes_test(es_veterinario)
def rechazar_solicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)
    solicitud.delete()
    return render(request, "main/infomsj.html", {
        "msj": "La solicitud fue rechazada."
    })