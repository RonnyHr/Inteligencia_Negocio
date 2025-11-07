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

        if Adopcion.objects.filter(mascota=mascota).exists():
            messages.error(request, 'La mascota seleccionada ya cuenta con una solicitud de adopción.')
            return redirect('nuevaAdopcion')
        
        Adopcion.objects.create(
            mascota=mascota,
            persona=persona,
            estado=estado,
            observaciones=observaciones,
            documento_pdf=documento_pdf,
        )
        messages.success(request, 'Solicitud de adopción registrada correctamente.')
    return redirect('nuevaAdopcion')


def editar_adopcion(request, pk):
    adopcion = get_object_or_404(Adopcion, pk=pk)
    mascotas_disponibles = Mascota.objects.filter(
        Q(adopciones__isnull=True) | Q(pk=adopcion.mascota_id)
    ).distinct()
    contexto = {
        'adopcion': adopcion,
        'mascotas': mascotas_disponibles,
        'personas': Persona.objects.all(),
    }
    return render(request, 'Adopcion/editarAdopcion.html', contexto)


def actualizar_adopcion(request, pk):
    adopcion = get_object_or_404(Adopcion, pk=pk)
    if request.method == 'POST':
        ruta_anterior = adopcion.documento_pdf.path if adopcion.documento_pdf else None
        mascota_id = request.POST.get('mascota')
        persona_id = request.POST.get('persona')
        mascota = get_object_or_404(Mascota, pk=mascota_id)
        if Adopcion.objects.filter(mascota=mascota).exclude(pk=adopcion.pk).exists():
            messages.error(request, 'La mascota seleccionada ya cuenta con una solicitud de adopción.')
            return redirect('editarAdopcion', pk=adopcion.pk)
        adopcion.mascota = mascota
        adopcion.persona = get_object_or_404(Persona, pk=persona_id)
        adopcion.estado = request.POST.get('estado')
        adopcion.observaciones = request.POST.get('observaciones')
        documento_pdf = request.FILES.get('documento_pdf')
        if documento_pdf:
            adopcion.documento_pdf = documento_pdf
        adopcion.save()
        if documento_pdf and ruta_anterior and os.path.isfile(ruta_anterior):
            try:
                os.remove(ruta_anterior)
            except OSError:
                pass
        messages.success(request, 'Solicitud de adopción actualizada correctamente.')
    return redirect('editarAdopcion', pk=adopcion.pk)


def eliminar_adopcion(request, pk):
    adopcion = get_object_or_404(Adopcion, pk=pk)
    ruta_archivo = adopcion.documento_pdf.path if adopcion.documento_pdf else None
    adopcion.delete()
    if ruta_archivo and os.path.isfile(ruta_archivo):
        try:
            os.remove(ruta_archivo)
        except OSError:
            pass
    messages.success(request, 'Solicitud de adopción eliminada correctamente.')
    return redirect('listaAdopcion')


def analisis_adopciones(request):
    total_mascotas = Mascota.objects.count()
    total_personas = Persona.objects.count()
    total_adopciones = Adopcion.objects.count()
    mascotas_disponibles = Mascota.objects.filter(adopciones__isnull=True).count()

    estado_qs = Adopcion.objects.values('estado').annotate(total=Count('id')).order_by('estado')
    estado_labels = [item['estado'] for item in estado_qs]
    estado_data = [item['total'] for item in estado_qs]

    mensual_qs = (
        Adopcion.objects.annotate(mes=TruncMonth('fecha_solicitud'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    mensual_labels = [
        item['mes'].strftime('%B %Y') if item['mes'] else 'Sin fecha'
        for item in mensual_qs
    ]
    mensual_data = [item['total'] for item in mensual_qs]