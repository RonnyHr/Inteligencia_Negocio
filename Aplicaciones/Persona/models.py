from django.db import models

# Create your models here.

class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    foto_perfil = models.FileField(upload_to='media/personas/perfiles/', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.nombres} {self.apellidos}"