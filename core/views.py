from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Termino, Variante
from .forms import TerminoForm


def home(request):
    """Buscador y listado principal."""
    if request.method == 'POST':
        form = TerminoForm(request.POST)
        if form.is_valid():
            termino = form.save()
            return redirect('termino_detail', slug=termino.palabra)
    else:
        form = TerminoForm()

    query = request.GET.get('q', '').strip()
    if query:
        terminos = Termino.objects.filter(
            Q(palabra__icontains=query) |
            Q(definicion__icontains=query) |
            Q(categoria_semantica__icontains=query)
        ).order_by('palabra')
    else:
        terminos = Termino.objects.all().order_by('-creado_en')[:20]

    return render(request, 'core/index.html', {
        'terminos': terminos,
        'query': query,
        'form': form,
        'total': Termino.objects.count(),
    })


def termino_detail(request, slug):
    """Mini vista de una palabra con todos sus campos lexicograficos."""
    termino = get_object_or_404(Termino, palabra__iexact=slug)
    variantes = termino.variantes.all().order_by('pais')

    # Terminos relacionados (misma categoria semantica)
    if termino.categoria_semantica:
        relacionados = Termino.objects.filter(
            categoria_semantica=termino.categoria_semantica
        ).exclude(id=termino.id)[:6]
    else:
        relacionados = Termino.objects.none()

    return render(request, 'core/termino_detail.html', {
        'termino': termino,
        'variantes': variantes,
        'relacionados': relacionados,
    })



# ═══════════════════════════════════════════════════════
# REGISTRO Y PERFIL
# ═══════════════════════════════════════════════════════

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PerfilForm
from .models import UserProfile


def registro(request):
    """Registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect('cursos:dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenido, ' + user.username + '!')
            return redirect('cursos:dashboard')
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {'form': form})


@login_required
def perfil(request):
    """Ver y editar el perfil del usuario."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=profile)

    return render(request, 'perfil.html', {
        'profile': profile,
        'form': form,
    })
