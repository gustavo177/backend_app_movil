from django.contrib import admin
from .models import Actor, Descripcion


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_usuario", "rol", "creado_en")
    list_filter = ("rol",)
    search_fields = ("nombre_usuario",)
    ordering = ("-creado_en",)


@admin.register(Descripcion)
class DescripcionAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "titulo", "creado_en")
    list_filter = ("creado_en", "actor__rol")
    search_fields = ("titulo", "descripcion", "actor__nombre_usuario")
    ordering = ("-creado_en",)


# admin.site.register(Perfil)

