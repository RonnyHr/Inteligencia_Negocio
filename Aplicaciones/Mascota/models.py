from django.db import models

# Create your models here.

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50, blank=True)
    edad = models.PositiveIntegerField(help_text="Edad aproximada en años")
    fecha_nacimiento = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True)
    foto_perfil = models.FileField(upload_to='media/mascotas/perfiles/', blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre
