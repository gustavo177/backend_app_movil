from django.db import models
from django.utils import timezone

class Actor(models.Model):
    ROL_CHOICES = (("usuario","Usuario"), ("admin","Administrador"))
    nombre_usuario = models.CharField(max_length=50, unique=True)
    contrasena     = models.CharField(max_length=255)
    rol            = models.CharField(max_length=20, choices=ROL_CHOICES, default="usuario")
    creado_en      = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "actor"   # 👈 sin managed=False

class Descripcion(models.Model):
    actor       = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="descripciones")
    titulo      = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen_url  = models.TextField(blank=True, null=True)
    creado_en   = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "descripcion"  # 👈 sin managed=False

# class Perfil(models.Model):
#     actor = models.OneToOneField('Actor', on_delete=models.CASCADE, related_name='perfil')
#     perfil = models.CharField(max_length=100)

#     class Meta:
#         db_table = "perfil"

#     def __str__(self):
#         return f"Perfil de {self.actor.nombre_usuario}"
