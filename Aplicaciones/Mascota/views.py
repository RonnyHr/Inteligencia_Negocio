import os

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Mascota


def lista_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'Mascota/inicio.html', {'mascotas': mascotas})