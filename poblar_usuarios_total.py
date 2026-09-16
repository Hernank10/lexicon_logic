"""
Poblar la base de datos con:
- 3 admins
- 9 profesores
- 96 estudiantes
- Inscripciones, progreso y certificados de prueba.

Uso:
    cd /d "E:\\02_proyectos\\lexicon_logic\\_original"
    E:\\PythonPortable_Django5\\python.exe manage.py shell -c "exec(open('poblar_usuarios_total.py', encoding='utf-8').read())"
"""
import random
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import UserProfile
from cursos.models import (
    Curso, Leccion, Ejercicio,
    Inscripcion, ProgresoLeccion, Certificado
)


PASSWORD = 'Test2026!'
random.seed(42)  # Para que sea reproducible


NOMBRES = [
    'Alberto', 'Miguel', 'Ana', 'Pedro', 'Andres', 'Laura', 'Carlos',
    'Sofia', 'Diego', 'Maria', 'Jose', 'Lucia', 'Javier', 'Elena',
    'Pablo', 'Carmen', 'Antonio', 'Isabel', 'Fernando', 'Rosa',
    'Raul', 'Beatriz', 'Manuel', 'Patricia', 'Francisco', 'Marta',
    'Ramon', 'Cristina', 'Vicente', 'Silvia', 'Emilio', 'Teresa',
]

APELLIDOS = [
    'Diaz', 'Fernandez', 'Castro', 'Alonso', 'Blanco', 'Gutierrez',
    'Garcia', 'Lopez', 'Martinez', 'Rodriguez', 'Perez', 'Sanchez',
    'Ramirez', 'Torres', 'Flores', 'Rivera', 'Vargas', 'Cruz',
    'Morales', 'Ortiz', 'Gomez', 'Herrera', 'Jimenez', 'Ruiz',
]

PAISES = [
    'Colombia', 'Mexico', 'Argentina', 'Espana', 'Peru',
    'Chile', 'Venezuela', 'Ecuador', 'Bolivia', 'Uruguay',
]


def crear_usuario(username, email, rol, first_name='', last_name='', is_staff=False, is_superuser=False):
    """Crea un usuario con su UserProfile."""
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
        }
    )
    if created:
        user.set_password(PASSWORD)
        user.save()

    # Crear/actualizar perfil
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.rol = rol
    profile.pais = random.choice(PAISES)
    profile.bio = 'Usuario de prueba del sistema Lexicon Logic.'
    profile.save()

    return user, created


def main():
    print('=' * 60)
    print('POBLANDO USUARIOS DE PRUEBA')
    print('=' * 60)

    # ─── 1. ADMINS ───
    print()
    print('[1/3] Creando 3 administradores...')
    admins = []
    for i in range(1, 4):
        username = f'admin{i}'
        email = f'{username}@lexicon.local'
        user, created = crear_usuario(
            username, email, 'admin',
            first_name=random.choice(NOMBRES),
            last_name=random.choice(APELLIDOS),
            is_staff=True, is_superuser=True
        )
        admins.append(user)
        estado = 'creado' if created else 'ya existe'
        print(f'  + {username} ({estado})')

    # ─── 2. PROFESORES ───
    print()
    print('[2/3] Creando 9 profesores...')
    profesores = []
    for i in range(1, 10):
        username = f'prof{i}'
        email = f'{username}@lexicon.local'
        first_name = random.choice(NOMBRES)
        last_name = random.choice(APELLIDOS)
        user, created = crear_usuario(
            username, email, 'profesor',
            first_name=first_name, last_name=last_name,
            is_staff=True, is_superuser=False
        )
        profesores.append(user)
        estado = 'creado' if created else 'ya existe'
        print(f'  + {username} ({first_name} {last_name}) [{estado}]')

    # ─── 3. ESTUDIANTES ───
    print()
    print('[3/3] Creando 96 estudiantes...')
    estudiantes = []
    for i in range(1, 97):
        username = f'est{i:03d}'
        email = f'{username}@lexicon.local'
        first_name = random.choice(NOMBRES)
        last_name = random.choice(APELLIDOS)
        user, created = crear_usuario(
            username, email, 'estudiante',
            first_name=first_name, last_name=last_name,
            is_staff=False, is_superuser=False
        )
        estudiantes.append(user)

    print(f'  + {len(estudiantes)} estudiantes creados (est001 a est096)')

    # ─── 4. INSCRIBIR ESTUDIANTES EN CURSOS ───
    print()
    print('=' * 60)
    print('INSCRIBIENDO ESTUDIANTES EN CURSOS')
    print('=' * 60)

    cursos = list(Curso.objects.all())
    if not cursos:
        print('  ERROR: No hay cursos. Ejecuta generar_cursos_lexicograficos.py primero.')
        return

    print(f'Cursos disponibles: {len(cursos)}')

    total_inscripciones = 0
    total_certificados = 0
    total_progresos = 0

    for estudiante in estudiantes:
        # Cada estudiante se inscribe en 1-3 cursos aleatorios
        num_cursos = random.randint(1, 3)
        cursos_elegidos = random.sample(cursos, min(num_cursos, len(cursos)))

        for curso in cursos_elegidos:
            inscripcion, creada = Inscripcion.objects.get_or_create(
                estudiante=estudiante,
                curso=curso,
            )
            if not creada:
                continue

            total_inscripciones += 1

            # Progreso aleatorio
            lecciones = list(curso.lecciones.all().order_by('orden'))
            if not lecciones:
                continue

            # Cuantas lecciones completar (0 a todas)
            probabilidad_completar = random.random()
            if probabilidad_completar < 0.2:
                # 20%: no completa nada
                num_completadas = 0
            elif probabilidad_completar < 0.6:
                # 40%: completa entre 1 y 2/3 del curso
                num_completadas = random.randint(1, max(1, int(len(lecciones) * 0.66)))
            else:
                # 40%: completa todo
                num_completadas = len(lecciones)

            for leccion in lecciones[:num_completadas]:
                progreso, _ = ProgresoLeccion.objects.get_or_create(
                    inscripcion=inscripcion,
                    leccion=leccion,
                )
                if not progreso.completada:
                    progreso.completada = True
                    progreso.xp_ganado = leccion.xp_reward
                    progreso.aciertos = random.randint(
                        max(1, leccion.ejercicios.count() - 2),
                        leccion.ejercicios.count()
                    )
                    progreso.errores = random.randint(0, 2)
                    progreso.fecha_completado = timezone.now()
                    progreso.save()
                    total_progresos += 1

                    inscripcion.xp_acumulado += leccion.xp_reward
                    inscripcion.save()

            # Actualizar progreso de la inscripcion
            inscripcion.actualizar_progreso()

            # Si completo todo, generar certificado
            if inscripcion.completado:
                cert, creado = Certificado.objects.get_or_create(
                    inscripcion=inscripcion,
                    defaults={
                        'xp_final': inscripcion.xp_acumulado,
                        'puntaje': random.randint(70, 100),
                    }
                )
                if creado:
                    total_certificados += 1

    # ─── 5. RESUMEN ───
    print()
    print('=' * 60)
    print('RESUMEN')
    print('=' * 60)
    print(f'Admins creados:      {len(admins)}')
    print(f'Profesores:          {len(profesores)}')
    print(f'Estudiantes:         {len(estudiantes)}')
    print()
    print(f'Inscripciones:       {total_inscripciones}')
    print(f'Progresos:           {total_progresos}')
    print(f'Certificados:        {total_certificados}')
    print()
    print(f'Contrasena comun:    {PASSWORD}')
    print()
    print('Usuarios de prueba:')
    print('  admin1, admin2, admin3')
    print('  prof1, prof2, ..., prof9')
    print('  est001, est002, ..., est096')
    print('=' * 60)


main()