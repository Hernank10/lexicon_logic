"""
URL configuration for lexicon_logic project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticacion
    path("accounts/login/",
         auth_views.LoginView.as_view(template_name="registration/login.html"),
         name="login"),
    path("accounts/logout/",
         auth_views.LogoutView.as_view(next_page="/"),
         name="logout"),
    path("accounts/registro/", views.registro, name="registro"),
    path("perfil/", views.perfil, name="perfil"),

    # Apps
    path("", views.home, name="home"),
    path("palabra/<str:slug>/", views.termino_detail, name="termino_detail"),
    path("cursos/", include("cursos.urls", namespace="cursos")),
]
