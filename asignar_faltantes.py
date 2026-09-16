from core.models import Termino

CATEGORIAS_FALTANTES = {
    # Pronombres
    'el': 'persona', 'tu': 'persona', 'ella': 'persona',
    'yo': 'persona', 'nosotros': 'persona',
    # Adverbios
    'alli': 'espacio', 'aqui': 'espacio', 'tambien': 'modalidad',
    'tampoco': 'modalidad', 'siempre': 'tiempo', 'nunca': 'tiempo',
    # Adjetivos
    'frio': 'naturaleza', 'caliente': 'naturaleza', 'rapido': 'valoracion',
    'lento': 'valoracion', 'bueno': 'valoracion', 'malo': 'valoracion',
    'grande': 'valoracion', 'nuevo': 'valoracion', 'libre': 'valoracion',
    'feliz': 'emocion', 'triste': 'emocion',
    # Verbos
    'ensenar': 'educacion', 'aprender': 'educacion',
    'estudiar': 'educacion', 'leer': 'comunicacion', 'escribir': 'comunicacion',
    'hablar': 'comunicacion', 'escuchar': 'comunicacion',
    'amar': 'emocion', 'odiar': 'emocion', 'reir': 'emocion', 'llorar': 'emocion',
    'vivir': 'existencia', 'morir': 'existencia', 'nacer': 'existencia',
    'crecer': 'existencia', 'cambiar': 'accion', 'trabajar': 'profesion',
    'jugar': 'accion', 'cantar': 'arte', 'bailar': 'arte',
    'comprar': 'accion', 'vender': 'accion',
    'abrir': 'accion', 'cerrar': 'accion', 'empezar': 'accion', 'terminar': 'accion',
    # Cuerpo humano
    'boca': 'persona', 'ojo': 'persona', 'pie': 'persona', 'mano': 'persona',
    'cabeza': 'persona', 'corazon': 'persona', 'brazo': 'persona',
    'pierna': 'persona', 'dedo': 'persona',
    # Conceptos
    'velocidad': 'fisica', 'peso': 'fisica', 'tamano': 'fisica',
    'forma': 'percepcion', 'color': 'percepcion', 'numero': 'matematicas',
    'sueno': 'cognicion',
    # Personas
    'nino': 'persona', 'medico': 'persona',
    # Geografia
    'pais': 'geografia', 'ciudad': 'geografia',
    # Alimentos
    'verdura': 'alimentacion', 'fruta': 'alimentacion', 'leche': 'alimentacion',
    'pan': 'alimentacion', 'comida': 'alimentacion',
}

def limpiar_palabra(p):
    p = p.lower().strip()
    reemplazos = {
        chr(225): 'a', chr(233): 'e', chr(237): 'i',
        chr(243): 'o', chr(250): 'u', chr(241): 'n',
    }
    for c, r in reemplazos.items():
        p = p.replace(c, r)
    return p

asignados = 0
sin_cat = []
for t in Termino.objects.all():
    if t.categoria_semantica:
        continue
    p = limpiar_palabra(t.palabra)
    if p in CATEGORIAS_FALTANTES:
        t.categoria_semantica = CATEGORIAS_FALTANTES[p]
        t.save()
        asignados += 1
    else:
        sin_cat.append(t.palabra)

print(f'Asignados: {asignados}')
print(f'Sin categoria: {len(sin_cat)}')
if sin_cat:
    print('Palabras sin categoria:')
    for p in sin_cat:
        print(f'  - {p}')

from collections import Counter
cats = Counter(Termino.objects.values_list('categoria_semantica', flat=True))
print()
print('Categorias:')
for cat, num in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {num}')
