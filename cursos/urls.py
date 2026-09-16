from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista'),

    # Estudiante
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle'),
    path('<int:curso_id>/inscribir/', views.inscribir_curso, name='inscribir'),
    path('leccion/<int:leccion_id>/', views.detalle_leccion, name='leccion'),
    path('leccion/<int:leccion_id>/completar/', views.completar_leccion, name='completar_leccion'),
    path('ejercicio/<int:ejercicio_id>/verificar/', views.verificar_ejercicio, name='verificar'),
    path('certificado/<int:cert_id>/', views.ver_certificado, name='certificado'),

    # Profesor — Dashboard y vistas
    path('profesor/', views.profesor_dashboard, name='profesor_dashboard'),
    path('profesor/cursos/', views.profesor_cursos, name='profesor_cursos'),
    path('profesor/curso/<int:curso_id>/', views.profesor_curso_detail, name='profesor_curso_detail'),
    path('profesor/estudiante/<int:estudiante_id>/', views.profesor_estudiante, name='profesor_estudiante'),
    path('profesor/ranking/', views.profesor_ranking, name='profesor_ranking'),

    # Profesor — CRUD Cursos
    path('profesor/curso/create/', views.profesor_curso_create, name='profesor_curso_create'),
    path('profesor/curso/<int:curso_id>/edit/', views.profesor_curso_edit, name='profesor_curso_edit'),
    path('profesor/curso/<int:curso_id>/delete/', views.profesor_curso_delete, name='profesor_curso_delete'),

    # Profesor — CRUD Lecciones
    path('profesor/curso/<int:curso_id>/leccion/create/',
         views.profesor_leccion_create, name='profesor_leccion_create'),
    path('profesor/leccion/<int:leccion_id>/edit/',
         views.profesor_leccion_edit, name='profesor_leccion_edit'),
    path('profesor/leccion/<int:leccion_id>/delete/',
         views.profesor_leccion_delete, name='profesor_leccion_delete'),
    path('profesor/leccion/<int:leccion_id>/',
         views.profesor_leccion_detail, name='profesor_leccion_detail'),

    # Profesor — CRUD Ejercicios
    path('profesor/leccion/<int:leccion_id>/ejercicio/create/',
         views.profesor_ejercicio_create, name='profesor_ejercicio_create'),
    path('profesor/ejercicio/<int:ejercicio_id>/edit/',
         views.profesor_ejercicio_edit, name='profesor_ejercicio_edit'),
    path('profesor/ejercicio/<int:ejercicio_id>/delete/',
         views.profesor_ejercicio_delete, name='profesor_ejercicio_delete'),

    # Profesor — Certificado manual
    path('profesor/certificado/<int:estudiante_id>/<int:curso_id>/otorgar/',
         views.profesor_otorgar_certificado, name='profesor_otorgar_certificado'),
]