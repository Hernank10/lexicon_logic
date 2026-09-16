import random
from collections import defaultdict
from core.models import Termino
from cursos.models import Curso, Leccion, Ejercicio


ICONOS = {
    'naturaleza': 'N', 'geografia': 'G', 'etica': 'E',
    'sociedad': 'S', 'astronomia': 'A', 'arte': 'R',
    'humanidades': 'H', 'ciencia': 'C', 'emocion': 'M',
    'comunicacion': 'K', 'fisica': 'F', 'educacion': 'U',
    'cultura': 'L', 'cognicion': 'O', 'persona': 'P',
    'literatura': 'T', 'linguistica': 'I', 'derecho': 'D',
    'psicologia': 'Y', 'gramatica': 'B', 'epistemologia': 'Q',
}


def generar():
    print('Generando cursos...')
    grupos = defaultdict(list)
    for t in Termino.objects.all():
        cat = t.categoria_semantica or 'general'
        grupos[cat].append(t)

    total_cursos = 0
    total_lecciones = 0
    total_ejercicios = 0

    for categoria, palabras in sorted(grupos.items(), key=lambda x: -len(x[1])):
        if len(palabras) < 1:
            continue

        icono = ICONOS.get(categoria.lower(), 'X')
        titulo = f"Vocabulario de {categoria.capitalize()}"

        curso, creado = Curso.objects.get_or_create(
            titulo=titulo,
            defaults={
                'descripcion': f"Aprende {len(palabras)} palabras de {categoria}",
                'icono': icono,
                'categoria_semantica': categoria,
                'nivel': 'basico',
            }
        )

        if not creado:
            print(f"  [ya existe] {titulo}")
            continue

        mitad = max(1, len(palabras) // 3)
        grupos_lecciones = [
            ('intro', 'Introduccion', palabras[:mitad]),
            ('practica', 'Practica', palabras[mitad:2*mitad]),
            ('evaluacion', 'Evaluacion', palabras[2*mitad:]),
        ]

        for i, (subclase, nombre, grupo) in enumerate(grupos_lecciones, 1):
            if not grupo:
                continue
            teoria = '\n'.join([f"- {p.palabra}: {p.definicion[:100]}" for p in grupo])
            leccion = Leccion.objects.create(
                curso=curso,
                titulo=f"{nombre} de {categoria}",
                subclase=subclase,
                orden=i,
                teoria=teoria,
                xp_reward=20 if subclase != 'evaluacion' else 30,
            )
            total_lecciones += 1

            for j, p in enumerate(grupo, 1):
                otras = [t for t in palabras if t.id != p.id]
                random.shuffle(otras)
                distractores = [o.palabra for o in otras[:3]]
                while len(distractores) < 3:
                    distractores.append('ninguna')

                correcta = random.choice(['A', 'B', 'C', 'D'])
                idx = ['A', 'B', 'C', 'D'].index(correcta)
                random.shuffle(distractores)
                finales = []
                di = 0
                for k in range(4):
                    if k == idx:
                        finales.append(p.palabra)
                    else:
                        finales.append(distractores[di])
                        di += 1

                Ejercicio.objects.create(
                    leccion=leccion,
                    termino=p,
                    orden=j,
                    pregunta=f"Cual es la palabra: {p.definicion[:100]}?",
                    opcion_a=finales[0],
                    opcion_b=finales[1],
                    opcion_c=finales[2],
                    opcion_d=finales[3],
                    respuesta_correcta=correcta,
                    explicacion=f"{p.palabra}: {p.definicion}",
                    xp_reward=10,
                )
                total_ejercicios += 1

        total_cursos += 1

    for c in Curso.objects.all():
        c.xp_total = sum(l.xp_reward for l in c.lecciones.all())
        c.save()

    print(f"Cursos creados: {total_cursos}")
    print(f"Lecciones: {total_lecciones}")
    print(f"Ejercicios: {total_ejercicios}")
    print(f"Total cursos BD: {Curso.objects.count()}")


generar()