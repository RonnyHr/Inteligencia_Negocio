import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Persona


def lista_persona(request):
    personas = Persona.objects.all()
    return render(request, 'Persona/inicio.html', {'personas': personas})  

def nueva_persona(request):
    return render(request, 'Persona/agregarPersona.html')

def guardar_persona(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        foto_perfil = request.FILES.get('foto_perfil')

        Persona.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            foto_perfil=foto_perfil,
        )