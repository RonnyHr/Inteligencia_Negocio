import json
import os

from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render

from Aplicaciones.Mascota.models import Mascota
from Aplicaciones.Persona.models import Persona

from .models import Adopcion


def lista_adopciones(request):
    adopciones = Adopcion.objects.select_related('mascota', 'persona').all()
    return render(request, 'Adopcion/inicio.html', {'adopciones': adopciones})


def nueva_adopcion(request):
    mascotas_disponibles = Mascota.objects.filter(adopciones__isnull=True)
    contexto = {
        'mascotas': mascotas_disponibles,
        'personas': Persona.objects.all(),
    }
    return render(request, 'Adopcion/agregarAdopcion.html', contexto)


def guardar_adopcion(request):
    if request.method == 'POST':
        mascota_id = request.POST.get('mascota')
        persona_id = request.POST.get('persona')
        estado = request.POST.get('estado')
        observaciones = request.POST.get('observaciones')
        documento_pdf = request.FILES.get('documento_pdf')

        mascota = get_object_or_404(Mascota, pk=mascota_id)
        persona = get_object_or_404(Persona, pk=persona_id)