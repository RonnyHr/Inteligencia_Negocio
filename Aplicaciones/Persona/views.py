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
        messages.success(request, 'Persona registrada correctamente.')
    return redirect('listaPersona')


def editar_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    return render(request, 'Persona/editarPersona.html', {'persona': persona})


def actualizar_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        ruta_anterior = persona.foto_perfil.path if persona.foto_perfil else None
        persona.nombres = request.POST.get('nombres')
        persona.apellidos = request.POST.get('apellidos')
        persona.direccion = request.POST.get('direccion')
        persona.telefono = request.POST.get('telefono')
        persona.correo = request.POST.get('correo')
        foto_perfil = request.FILES.get('foto_perfil')
        if foto_perfil:
            persona.foto_perfil = foto_perfil
        persona.save()
        if foto_perfil and ruta_anterior and os.path.isfile(ruta_anterior):
            try:
                os.remove(ruta_anterior)
            except OSError:
                pass
        messages.success(request, 'Persona actualizada correctamente.')
    return redirect('listaPersona')


def eliminar_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)