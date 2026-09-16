from django.contrib.auth.models import User
from cursos.models import Curso, Inscripcion


def main():
    user, created = User.objects.get_or_create(
        username='admin10',
        defaults={
            'email': 'admin10@lexicon.local',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        user.set_password('Test2026!')
        user.save()
        print('Usuario admin10 creado')
    else:
        print('Usuario admin10 ya existe')

    cursos = Curso.objects.all()[:5]
    for curso in cursos:
        insc, creada = Inscripcion.objects.get_or_create(
            estudiante=user,
            curso=curso,
        )
        if creada:
            print('Inscrito en: ' + curso.titulo)

    print('Total inscripciones: ' + str(Inscripcion.objects.filter(estudiante=user).count()))


main()