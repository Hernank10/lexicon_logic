from django.contrib import admin
from .models import Termino, Variante, UserProfile


@admin.register(Termino)
class TerminoAdmin(admin.ModelAdmin):
    list_display = ('palabra', 'categoria_gramatical', 'categoria_semantica', 'creado_en')
    list_filter = ('categoria_gramatical', 'nivel', 'dificultad')
    search_fields = ('palabra', 'definicion')


@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    list_display = ('palabra_variante', 'termino_base', 'pais', 'frecuencia_uso')
    list_filter = ('pais',)
    search_fields = ('palabra_variante',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'pais', 'creado_en')
    list_filter = ('rol', 'pais')
    search_fields = ('user__username', 'user__email')