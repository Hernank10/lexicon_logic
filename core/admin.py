from django.contrib import admin
from .models import Termino, Variante, UserProfile, Idioma, TraduccionTermino


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


@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ('nombre_nativo', 'codigo', 'familia', 'hablantes_millones', 'direccion', 'activo')
    list_filter = ('activo', 'direccion', 'familia')
    search_fields = ('nombre_nativo', 'nombre_ingles', 'codigo')
    ordering = ('-hablantes_millones',)


@admin.register(TraduccionTermino)
class TraduccionTerminoAdmin(admin.ModelAdmin):
    list_display = ('termino', 'idioma', 'traduccion', 'nivel_correspondencia', 'votos', 'verificado')
    list_filter = ('idioma', 'nivel_correspondencia', 'verificado')
    search_fields = ('termino__palabra', 'traduccion')
    autocomplete_fields = ('termino',)