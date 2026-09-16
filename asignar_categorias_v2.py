from core.models import Termino

CATEGORIAS = {
    # Naturaleza
    'tormenta': 'naturaleza', 'nube': 'naturaleza', 'frio': 'naturaleza',
    'calor': 'naturaleza', 'hielo': 'naturaleza', 'nieve': 'naturaleza',
    'lluvia': 'naturaleza', 'viento': 'naturaleza', 'fuego': 'naturaleza',
    'aire': 'naturaleza', 'cielo': 'naturaleza', 'lago': 'naturaleza',
    'rio': 'naturaleza', 'bosque': 'naturaleza', 'selva': 'naturaleza',
    'desierto': 'naturaleza', 'playa': 'naturaleza', 'montana': 'naturaleza',
    'valle': 'naturaleza', 'mar': 'naturaleza', 'sol': 'naturaleza',
    'tierra': 'astronomia', 'luna': 'astronomia', 'estrella': 'astronomia',
    'planeta': 'astronomia', 'galaxia': 'astronomia', 'universo': 'astronomia',
    'cometa': 'astronomia', 'meteoro': 'astronomia',
    'volcan': 'geografia', 'cordillera': 'geografia', 'bahia': 'geografia',
    'golfo': 'geografia', 'peninsula': 'geografia', 'oceano': 'geografia',
    'continente': 'geografia', 'isla': 'geografia',
    # Persona
    'nino': 'persona', 'mujer': 'persona', 'hombre': 'persona',
    'persona': 'persona', 'amigo': 'persona', 'familia': 'persona',
    'medico': 'persona', 'maestro': 'persona', 'estudiante': 'persona',
    'yo': 'persona', 'tu': 'persona', 'el': 'persona', 'ella': 'persona',
    # Sociedad
    'pueblo': 'sociedad', 'gobierno': 'sociedad', 'ley': 'sociedad',
    'justicia': 'sociedad', 'libertad': 'sociedad', 'paz': 'sociedad',
    'sociedad': 'sociedad', 'politica': 'sociedad', 'economia': 'sociedad',
    # Cultura
    'cultura': 'cultura', 'arte': 'arte', 'musica': 'arte',
    'literatura': 'literatura', 'teatro': 'arte', 'cine': 'arte',
    # Ciencia
    'ciencia': 'ciencia', 'fisica': 'ciencia', 'quimica': 'ciencia',
    'biologia': 'ciencia', 'medicina': 'ciencia', 'matematicas': 'ciencia',
    'tecnologia': 'ciencia',
    # Educacion
    'educacion': 'educacion', 'escuela': 'educacion', 'universidad': 'educacion',
    'estudio': 'educacion', 'conocimiento': 'educacion', 'libro': 'educacion',
    # Emocion
    'amor': 'emocion', 'felicidad': 'emocion', 'tristeza': 'emocion',
    'miedo': 'emocion', 'alegria': 'emocion', 'esperanza': 'emocion',
    # Cognicion
    'pensamiento': 'cognicion', 'idea': 'cognicion', 'memoria': 'cognicion',
    'razon': 'cognicion', 'inteligencia': 'cognicion', 'imaginacion': 'cognicion',
    'sueno': 'cognicion', 'duda': 'cognicion',
    # Existencia
    'vida': 'existencia', 'muerte': 'existencia', 'tiempo': 'existencia',
    'espacio': 'existencia',
    # Comunicacion
    'palabra': 'comunicacion', 'lengua': 'comunicacion',
    'lenguaje': 'comunicacion', 'idioma': 'comunicacion',
    # Linguistica
    'gramatica': 'linguistica', 'fonetica': 'linguistica',
    'linguistica': 'linguistica', 'semantica': 'linguistica',
    'sintaxis': 'linguistica',
    # Verbos
    'ser': 'accion', 'estar': 'accion', 'tener': 'accion', 'hacer': 'accion',
    'decir': 'comunicacion', 'ir': 'accion', 'ver': 'percepcion',
    'dar': 'accion', 'saber': 'cognicion', 'querer': 'volicion',
    'poder': 'modalidad', 'amar': 'emocion', 'vivir': 'existencia',
    'aprender': 'educacion', 'ensenar': 'educacion', 'crear': 'accion',
    'pensar': 'cognicion', 'escribir': 'comunicacion', 'leer': 'comunicacion',
    'hablar': 'comunicacion', 'comer': 'accion', 'beber': 'accion',
    'dormir': 'accion', 'caminar': 'accion', 'correr': 'accion',
    # Adjetivos
    'bueno': 'valoracion', 'grande': 'valoracion', 'nuevo': 'valoracion',
    'feliz': 'emocion', 'libre': 'valoracion', 'triste': 'emocion',
    'rapido': 'valoracion', 'lento': 'valoracion', 'caliente': 'naturaleza',
    # Adverbios
    'siempre': 'tiempo', 'nunca': 'tiempo', 'tambien': 'modalidad',
    'tampoco': 'modalidad', 'aqui': 'espacio', 'alli': 'espacio',
    # Vivienda
    'casa': 'vivienda', 'hogar': 'vivienda', 'edificio': 'vivienda',
    # Profesion
    'profesion': 'profesion', 'trabajo': 'profesion',
    # Medicina
    'salud': 'medicina', 'enfermedad': 'medicina',
    # Deporte
    'deporte': 'deporte',
    # Religion
    'fe': 'religion', 'religion': 'religion',
    # Filosofia
    'filosofia': 'filosofia', 'etica': 'filosofia', 'verdad': 'filosofia',
}

def normalizar(p):
    p = p.lower()
    reemplazos = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'n': 'n'}
    p = p.replace('a', 'a').replace('e', 'e').replace('i', 'i').replace('o', 'o').replace('u', 'u').replace('n', 'n')
    return p

asignados = 0
sin_cat = []
for t in Termino.objects.all():
    if t.categoria_semantica:
        continue
    p = t.palabra.lower()
    if p in CATEGORIAS:
        t.categoria_semantica = CATEGORIAS[p]
        t.save()
        asignados += 1
    else:
        sin_cat.append(t.palabra)

print(f'Asignados: {asignados}')
print(f'Sin categoria: {len(sin_cat)}')
if sin_cat:
    print('Palabras sin categoria:')
    for p in sin_cat[:30]:
        print(f'  - {p}')

from collections import Counter
cats = Counter(Termino.objects.values_list('categoria_semantica', flat=True))
print()
print('Categorias:')
for cat, num in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {num}')
