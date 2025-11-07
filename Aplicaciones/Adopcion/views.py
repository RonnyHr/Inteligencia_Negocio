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