from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from .models import Curso, Leccion, Ejercicio, Inscripcion, ProgresoLeccion, Certificado


def lista_cursos(request):
    cursos = Curso.objects.all()
    nivel = request.GET.get('nivel', '').strip()
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    return render(request, 'cursos/lista_cursos.html', {
        'cursos': cursos,
        'total_cursos': Curso.objects.count(),
        'total_lecciones': Leccion.objects.count(),
        'total_ejercicios': Ejercicio.objects.count(),
    })


def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    inscripcion = None
    if request.user.is_authenticated:
        inscripcion = Inscripcion.objects.filter(
            estudiante=request.user, curso=curso
        ).first()
    return render(request, 'cursos/detalle_curso.html', {
        'curso': curso,
        'lecciones': curso.lecciones.all().order_by('orden'),
        'inscripcion': inscripcion,
    })


def detalle_leccion(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    return render(request, 'cursos/detalle_leccion.html', {
        'leccion': leccion,
        'curso': leccion.curso,
        'ejercicios': leccion.ejercicios.all().order_by('orden'),
    })


@require_POST
def verificar_ejercicio(request, ejercicio_id):
    ej = get_object_or_404(Ejercicio, id=ejercicio_id)
    respuesta = request.POST.get('respuesta', '').strip().upper()
    correcta = ej.respuesta_correcta.upper()
    if respuesta == correcta:
        return HttpResponse(
            '<div class="alert alert-success"><strong>Correcto!</strong> +' + str(ej.xp_reward) + ' XP</div>'
        )
    return HttpResponse(
        '<div class="alert alert-danger"><strong>Incorrecto.</strong> Era: ' + correcta + '</div>'
    )


# ════════════════════════════════════════════════════════
# DASHBOARD Y GAMIFICACION
# ════════════════════════════════════════════════════════


@login_required
def dashboard(request):
    """Dashboard principal del estudiante con gamificacion."""
    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user
    ).select_related('curso')

    total_xp = inscripciones.aggregate(t=Sum('xp_acumulado'))['t'] or 0
    nivel_global = 1 + (total_xp // 100)
    xp_siguiente = 100 - (total_xp % 100)

    # Estadisticas globales
    cursos_completados = inscripciones.filter(completado=True).count()
    total_lecciones_completadas = ProgresoLeccion.objects.filter(
        inscripcion__estudiante=request.user, completada=True
    ).count()
    certificados = Certificado.objects.filter(
        inscripcion__estudiante=request.user
    ).count()

    # Cursos disponibles para inscribirse
    cursos_inscritos_ids = inscripciones.values_list('curso_id', flat=True)
    cursos_disponibles = Curso.objects.exclude(id__in=cursos_inscritos_ids)[:6]

    return render(request, 'cursos/dashboard.html', {
        'inscripciones': inscripciones,
        'total_xp': total_xp,
        'nivel_global': nivel_global,
        'xp_siguiente': xp_siguiente,
        'cursos_completados': cursos_completados,
        'total_lecciones_completadas': total_lecciones_completadas,
        'certificados': certificados,
        'cursos_disponibles': cursos_disponibles,
    })


@login_required
def inscribir_curso(request, curso_id):
    """Inscribe al estudiante en un curso."""
    curso = get_object_or_404(Curso, id=curso_id)
    inscripcion, creada = Inscripcion.objects.get_or_create(
        estudiante=request.user,
        curso=curso,
    )
    if creada:
        messages.success(request, f'Te has inscrito en "{curso.titulo}"')
    else:
        messages.info(request, f'Ya estabas inscrito en "{curso.titulo}"')
    return redirect('cursos:detalle', curso_id=curso.id)


@login_required
@require_POST
def completar_leccion(request, leccion_id):
    """Marca una leccion como completada y otorga XP."""
    leccion = get_object_or_404(Leccion, id=leccion_id)
    inscripcion = get_object_or_404(
        Inscripcion, estudiante=request.user, curso=leccion.curso
    )
    progreso, creado = ProgresoLeccion.objects.get_or_create(
        inscripcion=inscripcion, leccion=leccion
    )
    if not progreso.completada:
        progreso.completada = True
        progreso.xp_ganado = leccion.xp_reward
        progreso.fecha_completado = timezone.now()
        progreso.save()

        inscripcion.xp_acumulado += leccion.xp_reward
        inscripcion.save()
        inscripcion.actualizar_progreso()

        # Otorgar certificado si completo todo
        if inscripcion.completado:
            Certificado.objects.get_or_create(
                inscripcion=inscripcion,
                defaults={
                    'xp_final': inscripcion.xp_acumulado,
                    'puntaje': 100,
                }
            )

    return redirect('cursos:leccion', leccion_id=leccion.id)


@login_required
def ver_certificado(request, cert_id):
    """Muestra un certificado."""
    certificado = get_object_or_404(
        Certificado, id=cert_id, inscripcion__estudiante=request.user
    )
    return render(request, 'cursos/certificado.html', {
        'certificado': certificado,
    })


# ═══════════════════════════════════════════════════════
# DASHBOARD DEL PROFESOR
# ═══════════════════════════════════════════════════════

from django.db.models import Count, Avg, Q


@login_required
def profesor_dashboard(request):
    """Dashboard principal del profesor con estadisticas y gamificacion."""
    # Verificar que es profesor o admin
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        messages.error(request, 'Acceso solo para profesores.')
        return redirect('cursos:dashboard')

    # KPIs globales
    total_cursos = Curso.objects.count()
    total_lecciones = Leccion.objects.count()
    total_ejercicios = Ejercicio.objects.count()
    total_estudiantes = User.objects.filter(profile__rol='estudiante').count()
    total_inscripciones = Inscripcion.objects.count()
    total_certificados = Certificado.objects.count()

    # Estudiantes con su gamificacion
    estudiantes = User.objects.filter(
        profile__rol='estudiante'
    ).annotate(
        num_inscripciones=Count('inscripciones', distinct=True),
        xp_total=Sum('inscripciones__xp_acumulado'),
        num_certificados=Count('inscripciones__certificado', distinct=True),
    ).order_by('-xp_total')[:50]

    # Calcular nivel para cada estudiante
    for e in estudiantes:
        xp = e.xp_total or 0
        e.nivel = 1 + (xp // 100)
        e.progreso_siguiente = xp % 100

    # Cursos con estadisticas
    cursos_stats = Curso.objects.annotate(
        num_inscritos=Count('inscripciones', distinct=True),
        num_lecciones_curso=Count('lecciones', distinct=True),
        xp_total_curso=Sum('inscripciones__xp_acumulado'),
    ).order_by('-num_inscritos')[:20]

    # Certificados recientes
    certificados_recientes = Certificado.objects.select_related(
        'inscripcion__estudiante', 'inscripcion__curso'
    ).order_by('-fecha_emision')[:10]

    return render(request, 'cursos/profesor_dashboard.html', {
        'total_cursos': total_cursos,
        'total_lecciones': total_lecciones,
        'total_ejercicios': total_ejercicios,
        'total_estudiantes': total_estudiantes,
        'total_inscripciones': total_inscripciones,
        'total_certificados': total_certificados,
        'estudiantes': estudiantes,
        'cursos_stats': cursos_stats,
        'certificados_recientes': certificados_recientes,
    })


@login_required
def profesor_estudiante(request, estudiante_id):
    """Detalle de un estudiante: sus cursos, XP, certificados."""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        return redirect('cursos:dashboard')

    estudiante = get_object_or_404(User, id=estudiante_id)
    inscripciones = Inscripcion.objects.filter(
        estudiante=estudiante
    ).select_related('curso')

    total_xp = inscripciones.aggregate(t=Sum('xp_acumulado'))['t'] or 0
    nivel = 1 + (total_xp // 100)

    # Lecciones completadas por el estudiante
    progresos = ProgresoLeccion.objects.filter(
        inscripcion__estudiante=estudiante,
        completada=True
    ).select_related('leccion__curso')[:20]

    # Certificados del estudiante
    certificados = Certificado.objects.filter(
        inscripcion__estudiante=estudiante
    ).select_related('inscripcion__curso')

    return render(request, 'cursos/profesor_estudiante.html', {
        'estudiante': estudiante,
        'inscripciones': inscripciones,
        'total_xp': total_xp,
        'nivel': nivel,
        'progresos': progresos,
        'certificados': certificados,
    })


@login_required
@require_POST
def profesor_otorgar_certificado(request, estudiante_id, curso_id):
    """Otorga un certificado manualmente a un estudiante."""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        return redirect('cursos:dashboard')

    estudiante = get_object_or_404(User, id=estudiante_id)
    curso = get_object_or_404(Curso, id=curso_id)

    # Buscar o crear la inscripcion
    inscripcion, _ = Inscripcion.objects.get_or_create(
        estudiante=estudiante,
        curso=curso,
    )

    # Marcar como completado
    inscripcion.completado = True
    inscripcion.progreso = 100
    inscripcion.save()

    # Otorgar certificado
    cert, creado = Certificado.objects.get_or_create(
        inscripcion=inscripcion,
        defaults={
            'xp_final': inscripcion.xp_acumulado,
            'puntaje': 100,
        }
    )
    if creado:
        messages.success(request, 'Certificado otorgado a ' + estudiante.username)
    else:
        messages.info(request, 'Ya tenia certificado')

    return redirect('cursos:profesor_dashboard')


@login_required
def profesor_cursos(request):
    """Listado de cursos con estadisticas para el profesor."""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        return redirect('cursos:dashboard')

    cursos = Curso.objects.annotate(
        num_inscritos=Count('inscripciones', distinct=True),
        num_lecciones_curso=Count('lecciones', distinct=True),
        num_completados=Count('inscripciones', filter=Q(inscripciones__completado=True), distinct=True),
    ).order_by('-num_inscritos')

    return render(request, 'cursos/profesor_cursos.html', {
        'cursos': cursos,
    })


@login_required
def profesor_curso_detail(request, curso_id):
    """Detalle de un curso para el profesor con lista de inscritos."""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        return redirect('cursos:dashboard')

    curso = get_object_or_404(Curso, id=curso_id)
    inscritos = Inscripcion.objects.filter(
        curso=curso
    ).select_related('estudiante', 'estudiante__profile').order_by('-xp_acumulado')

    # Estadisticas del curso
    total_inscritos = inscritos.count()
    completados = inscritos.filter(completado=True).count()
    xp_promedio = inscritos.aggregate(a=Avg('xp_acumulado'))['a'] or 0

    return render(request, 'cursos/profesor_curso_detail.html', {
        'curso': curso,
        'inscritos': inscritos,
        'total_inscritos': total_inscritos,
        'completados': completados,
        'xp_promedio': round(xp_promedio),
    })


@login_required
def profesor_ranking(request):
    """Ranking global de estudiantes."""
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.rol not in ('profesor', 'admin'):
        return redirect('cursos:dashboard')

    ranking = User.objects.filter(
        profile__rol='estudiante'
    ).annotate(
        xp_total=Sum('inscripciones__xp_acumulado'),
        num_certificados=Count('inscripciones__certificado', distinct=True),
        num_cursos=Count('inscripciones', distinct=True),
    ).filter(xp_total__gt=0).order_by('-xp_total')[:100]

    for i, est in enumerate(ranking, 1):
        est.posicion = i
        est.nivel = 1 + ((est.xp_total or 0) // 100)

    return render(request, 'cursos/profesor_ranking.html', {
        'ranking': ranking,
    })



# ═══════════════════════════════════════════════════════
# CRUD DE CURSOS (PROFESOR)
# ═══════════════════════════════════════════════════════

from .forms import CursoForm, LeccionForm, EjercicioForm


def _verificar_profesor(request):
    """Helper: retorna True si es profesor o admin."""
    profile = getattr(request.user, 'profile', None)
    return profile and profile.rol in ('profesor', 'admin')


@login_required
def profesor_curso_create(request):
    """Crear curso nuevo."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save()
            messages.success(request, 'Curso creado: ' + curso.titulo)
            return redirect('cursos:profesor_dashboard')
    else:
        form = CursoForm()

    return render(request, 'cursos/profesor_curso_form.html', {
        'form': form,
        'titulo': 'Crear curso nuevo',
        'accion': 'Crear',
    })


@login_required
def profesor_curso_edit(request, curso_id):
    """Editar curso existente."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado: ' + curso.titulo)
            return redirect('cursos:profesor_curso_detail', curso_id=curso.id)
    else:
        form = CursoForm(instance=curso)

    return render(request, 'cursos/profesor_curso_form.html', {
        'form': form,
        'titulo': 'Editar curso',
        'accion': 'Guardar cambios',
        'curso': curso,
    })


@login_required
@require_POST
def profesor_curso_delete(request, curso_id):
    """Eliminar curso."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    curso = get_object_or_404(Curso, id=curso_id)
    titulo = curso.titulo
    curso.delete()
    messages.success(request, 'Curso eliminado: ' + titulo)
    return redirect('cursos:profesor_dashboard')


# ═══════════════════════════════════════════════════════
# CRUD DE LECCIONES (PROFESOR)
# ═══════════════════════════════════════════════════════


@login_required
def profesor_leccion_create(request, curso_id):
    """Crear leccion en un curso."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        form = LeccionForm(request.POST)
        if form.is_valid():
            leccion = form.save(commit=False)
            leccion.curso = curso
            leccion.save()
            messages.success(request, 'Leccion creada: ' + leccion.titulo)
            return redirect('cursos:profesor_curso_detail', curso_id=curso.id)
    else:
        # Pre-llenar orden con el siguiente numero
        siguiente = curso.lecciones.count() + 1
        form = LeccionForm(initial={'orden': siguiente, 'xp_reward': 20})

    return render(request, 'cursos/profesor_leccion_form.html', {
        'form': form,
        'curso': curso,
        'titulo': 'Crear leccion en ' + curso.titulo,
        'accion': 'Crear',
    })


@login_required
def profesor_leccion_edit(request, leccion_id):
    """Editar leccion existente."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    leccion = get_object_or_404(Leccion, id=leccion_id)

    if request.method == 'POST':
        form = LeccionForm(request.POST, instance=leccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leccion actualizada: ' + leccion.titulo)
            return redirect('cursos:profesor_curso_detail', curso_id=leccion.curso.id)
    else:
        form = LeccionForm(instance=leccion)

    return render(request, 'cursos/profesor_leccion_form.html', {
        'form': form,
        'curso': leccion.curso,
        'leccion': leccion,
        'titulo': 'Editar leccion',
        'accion': 'Guardar cambios',
    })


@login_required
@require_POST
def profesor_leccion_delete(request, leccion_id):
    """Eliminar leccion."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    leccion = get_object_or_404(Leccion, id=leccion_id)
    curso_id = leccion.curso.id
    titulo = leccion.titulo
    leccion.delete()
    messages.success(request, 'Leccion eliminada: ' + titulo)
    return redirect('cursos:profesor_curso_detail', curso_id=curso_id)


# ═══════════════════════════════════════════════════════
# CRUD DE EJERCICIOS (PROFESOR)
# ═══════════════════════════════════════════════════════


@login_required
def profesor_ejercicio_create(request, leccion_id):
    """Crear ejercicio en una leccion."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    leccion = get_object_or_404(Leccion, id=leccion_id)

    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=False)
            ejercicio.leccion = leccion
            ejercicio.save()
            messages.success(request, 'Ejercicio creado')
            return redirect('cursos:profesor_leccion_detail', leccion_id=leccion.id)
    else:
        siguiente = leccion.ejercicios.count() + 1
        form = EjercicioForm(initial={'orden': siguiente, 'xp_reward': 10})

    return render(request, 'cursos/profesor_ejercicio_form.html', {
        'form': form,
        'leccion': leccion,
        'curso': leccion.curso,
        'titulo': 'Crear ejercicio en ' + leccion.titulo,
        'accion': 'Crear',
    })


@login_required
def profesor_ejercicio_edit(request, ejercicio_id):
    """Editar ejercicio existente."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)

    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio actualizado')
            return redirect('cursos:profesor_leccion_detail', leccion_id=ejercicio.leccion.id)
    else:
        form = EjercicioForm(instance=ejercicio)

    return render(request, 'cursos/profesor_ejercicio_form.html', {
        'form': form,
        'leccion': ejercicio.leccion,
        'curso': ejercicio.leccion.curso,
        'ejercicio': ejercicio,
        'titulo': 'Editar ejercicio',
        'accion': 'Guardar cambios',
    })


@login_required
@require_POST
def profesor_ejercicio_delete(request, ejercicio_id):
    """Eliminar ejercicio."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    leccion_id = ejercicio.leccion.id
    ejercicio.delete()
    messages.success(request, 'Ejercicio eliminado')
    return redirect('cursos:profesor_leccion_detail', leccion_id=leccion_id)


@login_required
def profesor_leccion_detail(request, leccion_id):
    """Vista detallada de una leccion con sus ejercicios (para profesor)."""
    if not _verificar_profesor(request):
        return redirect('cursos:dashboard')

    leccion = get_object_or_404(Leccion, id=leccion_id)
    return render(request, 'cursos/profesor_leccion_detail.html', {
        'leccion': leccion,
        'curso': leccion.curso,
        'ejercicios': leccion.ejercicios.all().order_by('orden'),
    })