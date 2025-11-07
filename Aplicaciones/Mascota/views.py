import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Mascota


def lista_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'Mascota/inicio.html', {'mascotas': mascotas})


def nueva_mascota(request):
    return render(request, 'Mascota/nuevaMascota.html')


def guardar_mascota(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        descripcion = request.POST.get('descripcion')
        foto_perfil = request.FILES.get('foto_perfil')

        Mascota.objects.create(
            nombre=nombre,
            especie=especie,
            raza=raza,
            edad=edad,
            fecha_nacimiento=fecha_nacimiento,
            descripcion=descripcion,
            foto_perfil=foto_perfil,
        )
        messages.success(request, 'Mascota registrada correctamente.')
    return redirect('listaMascota')


def editar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    return render(request, 'Mascota/editarMascota.html', {'mascota': mascota})


def actualizar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        ruta_anterior = mascota.foto_perfil.path if mascota.foto_perfil else None
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.raza = request.POST.get('raza')
        mascota.edad = request.POST.get('edad')
        mascota.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        mascota.descripcion = request.POST.get('descripcion')
        foto_perfil = request.FILES.get('foto_perfil')
        if foto_perfil:
            mascota.foto_perfil = foto_perfil
        mascota.save()
        if foto_perfil and ruta_anterior and os.path.isfile(ruta_anterior):
            try:
                os.remove(ruta_anterior)
            except OSError:
                pass
        messages.success(request, 'Mascota actualizada correctamente.')
    return redirect('listaMascota')


def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)
    if mascota.adopciones.exists():
        messages.error(request, 'No se puede eliminar la mascota porque está asociada a solicitudes de adopción.')
    else:
        ruta_archivo = mascota.foto_perfil.path if mascota.foto_perfil else None
        mascota.delete()