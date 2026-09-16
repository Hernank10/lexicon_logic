"""
Agrega N preguntas por leccion sin duplicar.
"""
from cursos.models import Leccion, Ejercicio
from core.models import Termino
import random


PREGUNTAS_POR_LECCION = 30
XP_POR_PREGUNTA = 10
random.seed(42)


def limpiar(p):
    p = p.lower().strip()
    for c, r in [(chr(225),"a"),(chr(233),"e"),(chr(237),"i"),(chr(243),"o"),(chr(250),"u"),(chr(241),"n")]:
        p = p.replace(c, r)
    return p


print("=" * 60)
print(f"AGREGANDO {PREGUNTAS_POR_LECCION} PREGUNTAS POR LECCION")
print("=" * 60)

lecciones = list(Leccion.objects.all())
terminos = list(Termino.objects.all())
print(f"Lecciones: {len(lecciones)}")
print(f"Terminos disponibles: {len(terminos)}")
print(f"Ejercicios antes: {Ejercicio.objects.count()}")
print()

total_creadas = 0

for i, leccion in enumerate(lecciones, 1):
    existentes = leccion.ejercicios.count()
    faltantes = PREGUNTAS_POR_LECCION - existentes
    
    if faltantes <= 0:
        print(f"  [{i}/{len(lecciones)}] {leccion.titulo[:40]}: ya tiene {existentes}")
        continue
    
    creadas = 0
    usados = set()
    
    for n in range(existentes + 1, PREGUNTAS_POR_LECCION + 1):
        if not terminos:
            break
        
        # Elegir termino no usado
        intentos = 0
        termino = None
        while intentos < 50:
            t = random.choice(terminos)
            if t.id not in usados:
                termino = t
                usados.add(t.id)
                break
            intentos += 1
        
        if not termino:
            termino = random.choice(terminos)
        
        # Opciones
        otras = [t for t in terminos if t.id != termino.id]
        random.shuffle(otras)
        distractores = [o.palabra for o in otras[:3]]
        while len(distractores) < 3:
            distractores.append("ninguna")
        
        correcta = random.choice(["A", "B", "C", "D"])
        idx = ["A", "B", "C", "D"].index(correcta)
        random.shuffle(distractores)
        finales = []
        di = 0
        for k in range(4):
            if k == idx:
                finales.append(termino.palabra)
            else:
                finales.append(distractores[di])
                di += 1
        
        Ejercicio.objects.create(
            leccion=leccion,
            termino=termino,
            orden=n,
            pregunta=f"Cual es la palabra: {termino.definicion[:100]}?",
            opcion_a=finales[0],
            opcion_b=finales[1],
            opcion_c=finales[2],
            opcion_d=finales[3],
            respuesta_correcta=correcta,
            explicacion=f"{termino.palabra}: {termino.definicion}",
            xp_reward=XP_POR_PREGUNTA,
        )
        creadas += 1
    
    total_creadas += creadas
    print(f"  [{i}/{len(lecciones)}] {leccion.titulo[:40]}: +{creadas} (total: {leccion.ejercicios.count()})")

print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Lecciones procesadas: {len(lecciones)}")
print(f"Preguntas creadas: {total_creadas}")
print(f"Total en BD: {Ejercicio.objects.count()}")
print("=" * 60)
