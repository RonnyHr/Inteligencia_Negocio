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