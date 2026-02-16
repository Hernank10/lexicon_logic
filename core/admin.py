from django.contrib import admin
from .models import Termino, Variante

# Configuración avanzada para ver las variantes dentro del término en el admin
class VarianteInline(admin.TabularInline):
    model = Variante
    extra = 1

@admin.register(Termino)
class TerminoAdmin(admin.ModelAdmin):
    list_display = ('palabra', 'categoria_gramatical', 'creado_en')
    search_fields = ('palabra',)
    inlines = [VarianteInline]

@admin.register(Variante)
class VarianteAdmin(admin.ModelAdmin):
    list_display = ('palabra_variante', 'termino_base', 'pais', 'frecuencia_uso')
    list_filter = ('pais', 'termino_base')
    search_fields = ('palabra_variante', 'pais')
