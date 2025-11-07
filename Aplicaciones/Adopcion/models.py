from django.core.validators import FileExtensionValidator
from django.db import models


class Adopcion(models.Model):
    mascota = models.ForeignKey('Mascota.Mascota', on_delete=models.CASCADE, related_name='adopciones')
    persona = models.ForeignKey('Persona.Persona', on_delete=models.CASCADE, related_name='solicitudes_adopcion')
    fecha_solicitud = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='pendiente')
    observaciones = models.TextField(blank=True)
    documento_pdf = models.FileField(
        upload_to='media/adopciones/documentos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf'])],
    )

    def __str__(self) -> str:
        return f"{self.persona} - {self.mascota} ({self.estado})"

