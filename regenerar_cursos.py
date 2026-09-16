"""
Borra los cursos actuales y los regenera con las categorías corregidas.
"""
from collections import defaultdict
from core.models import Termino
from cursos.models import Curso, Leccion, Ejercicio


def main():
    print('=' * 60)
    print('REGENERANDO CURSOS')
    print('=' * 60)
    
    # 1. Borrar cursos actuales
    total_cursos_antes = Curso.objects.count()
    print(f'Cursos antes: {total_cursos_antes}')
    
    Curso.objects.all().delete()
    print('Cursos borrados')
    print()
    
    # 2. Agrupar términos por categoría semántica corregida
    grupos = defaultdict(list)
    for t in Termino.objects.all():
        cat = t.categoria_semantica or 'general'
        grupos[cat].append(t)
    
    print(f'Categorías encontradas: {len(grupos)}')
    print()
    
    # 3. Crear un curso por categoría
    total_cursos = 0
    total_lecciones = 0
    total_ejercicios = 0
    
    for categoria, palabras in sorted(grupos.items(), key=lambda x: -len(x[1])):
        if len(palabras) < 2:
            continue
        
        # Crear curso
        titulo = f'Vocabulario de {categoria.capitalize()}'
        curso = Curso.objects.create(
            titulo=titulo,
            descripcion=f'Aprende {len(palabras)} palabras de {categoria}',
            icono='X',
            categoria_semantica=categoria,
            nivel='basico',
        )
        total_cursos += 1
        print(f'  Curso: {titulo} ({len(palabras)} palabras)')
        
        # Dividir en 3 lecciones
        tamano = max(1, len(palabras) // 3)
        grupos_lecciones = [
            ('intro', 'Introducción', palabras[:tamano]),
            ('practica', 'Práctica', palabras[tamano:2*tamano]),
            ('evaluacion', 'Evaluación', palabras[2*tamano:]),
        ]
        
        for i, (subclase, nombre, grupo) in enumerate(grupos_lecciones, 1):
            if not grupo:
                continue
            
            teoria = '\n'.join([f'- {p.palabra}: {p.definicion[:100]}' for p in grupo])
            
            leccion = Leccion.objects.create(
                curso=curso,
                titulo=f'{nombre} de {categoria}',
                subclase=subclase,
                orden=i,
                teoria=teoria,
                xp_reward=20 if subclase != 'evaluacion' else 30,
            )
            total_lecciones += 1
            
            # Crear un ejercicio por palabra
            for j, p in enumerate(grupo, 1):
                # Opciones incorrectas
                otras = [x for x in palabras if x.id != p.id][:3]
                distractores = [o.palabra for o in otras]
                while len(distractores) < 3:
                    distractores.append('ninguna')
                
                Ejercicio.objects.create(
                    leccion=leccion,
                    termino=p,
                    orden=j,
                    pregunta=f'¿Cuál es la palabra: {p.definicion[:100]}?',
                    opcion_a=p.palabra,
                    opcion_b=distractores[0],
                    opcion_c=distractores[1],
                    opcion_d=distractores[2],
                    respuesta_correcta='A',
                    explicacion=f'{p.palabra}: {p.definicion}',
                    xp_reward=10,
                )
                total_ejercicios += 1
    
    # 4. Resumen
    print()
    print('=' * 60)
    print('RESUMEN')
    print('=' * 60)
    print(f'Cursos creados:     {total_cursos}')
    print(f'Lecciones creadas:  {total_lecciones}')
    print(f'Ejercicios creados: {total_ejercicios}')
    print()
    print(f'Total cursos BD:    {Curso.objects.count()}')
    print(f'Total lecciones:    {Leccion.objects.count()}')
    print(f'Total ejercicios:   {Ejercicio.objects.count()}')
    print('=' * 60)


main()