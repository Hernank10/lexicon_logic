from django.contrib import admin
from .models import Curso, Leccion, Ejercicio


class LeccionInline(admin.TabularInline):
    model = Leccion
    extra = 1


class EjercicioInline(admin.TabularInline):
    model = Ejercicio
    extra = 1


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'icono', 'categoria_semantica', 'nivel', 'xp_total')
    list_filter = ('nivel', 'categoria_semantica')
    search_fields = ('titulo',)
    inlines = [LeccionInline]


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'subclase', 'orden')
    list_filter = ('subclase', 'curso')
    inlines = [EjercicioInline]


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'leccion', 'respuesta_correcta')
    list_filter = ('leccion__curso',)