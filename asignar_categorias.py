"""
Asigna categorias semanticas a los 121 terminos.
"""
from core.models import Termino


# Mapa palabra -> categoria semantica
CATEGORIAS = {
    # Naturaleza
    'tormenta': 'naturaleza', 'nube': 'naturaleza', 'frío': 'naturaleza',
    'calor': 'naturaleza', 'hielo': 'naturaleza', 'nieve': 'naturaleza',
    'lluvia': 'naturaleza', 'viento': 'naturaleza', 'fuego': 'naturaleza',
    'aire': 'naturaleza', 'cielo': 'naturaleza', 'lago': 'naturaleza',
    'río': 'naturaleza', 'bosque': 'naturaleza', 'selva': 'naturaleza',
    'desierto': 'naturaleza', 'playa': 'naturaleza', 'isla': 'naturaleza',
    'montaña': 'naturaleza', 'valle': 'naturaleza', 'mar': 'naturaleza',
    'sol': 'naturaleza', 'luna': 'astronomía', 'estrella': 'astronomía',
    'planeta': 'astronomía', 'tierra': 'astronomía', 'galaxia': 'astronomía',
    'universo': 'astronomía', 'cometa': 'astronomía', 'meteoro': 'astronomía',
    'volcán': 'geografía', 'cordillera': 'geografía', 'bahía': 'geografía',
    'golfo': 'geografía', 'península': 'geografía', 'océano': 'geografía',
    'continente': 'geografía', 'isla': 'geografía',
    
    # Persona
    'niño': 'persona', 'mujer': 'persona', 'hombre': 'persona',
    'persona': 'persona', 'amigo': 'persona', 'familia': 'persona',
    'médico': 'persona', 'maestro': 'persona', 'estudiante': 'persona',
    
    # Sociedad
    'pueblo': 'sociedad', 'gobierno': 'sociedad', 'ley': 'sociedad',
    'justicia': 'sociedad', 'libertad': 'sociedad', 'paz': 'sociedad',
    'sociedad': 'sociedad', 'política': 'sociedad', 'economía': 'sociedad',
    'cultura': 'cultura', 'arte': 'arte', 'música': 'arte',
    'literatura': 'literatura', 'teatro': 'arte', 'cine': 'arte',
    
    # Ciencia
    'ciencia': 'ciencia', 'física': 'ciencia', 'química': 'ciencia',
    'biología': 'ciencia', 'medicina': 'ciencia', 'matemáticas': 'ciencia',
    'tecnología': 'ciencia',
    
    # Educación
    'educación': 'educación', 'escuela': 'educación', 'universidad': 'educación',
    'estudio': 'educación', 'conocimiento': 'educación', 'libro': 'educación',
    
    # Emoción
    'amor': 'emoción', 'felicidad': 'emoción', 'tristeza': 'emoción',
    'miedo': 'emoción', 'alegría': 'emoción', 'esperanza': 'emoción',
    
    # Cognición
    'pensamiento': 'cognición', 'idea': 'cognición', 'memoria': 'cognición',
    'razón': 'cognición', 'inteligencia': 'cognición', 'imaginación': 'cognición',
    'sueño': 'cognición', 'duda': 'cognición',
    
    # Existencia
    'vida': 'existencia', 'muerte': 'existencia', 'tiempo': 'existencia',
    'espacio': 'existencia', 'ser': 'existencia',
    
    # Comunicación
    'palabra': 'comunicación', 'lengua': 'comunicación', 'comunicación': 'comunicación',
    'lenguaje': 'comunicación', 'idioma': 'comunicación',
    
    # Lingüística
    'gramática': 'lingüística', 'fonética': 'lingüística', 'lingüística': 'lingüística',
    'semántica': 'lingüística', 'sintaxis': 'lingüística',
    
    # Verbos y acciones
    'ser': 'acción', 'estar': 'acción', 'tener': 'acción', 'hacer': 'acción',
    'decir': 'comunicación', 'ir': 'acción', 'ver': 'percepción',
    'dar': 'acción', 'saber': 'cognición', 'querer': 'volición',
    'poder': 'modalidad', 'amar': 'emoción', 'vivir': 'existencia',
    'aprender': 'educación', 'enseñar': 'educación', 'crear': 'acción',
    'pensar': 'cognición', 'escribir': 'comunicación', 'leer': 'comunicación',
    'hablar': 'comunicación', 'comer': 'acción', 'beber': 'acción',
    'dormir': 'acción', 'caminar': 'acción', 'correr': 'acción',
    
    # Adjetivos
    'bueno': 'valoración', 'grande': 'valoración', 'nuevo': 'valoración',
    'feliz': 'emoción', 'libre': 'valoración', 'triste': 'emoción',
    'rápido': 'valoración', 'lento': 'valoración', 'frío': 'naturaleza',
    'caliente': 'naturaleza',
    
    # Adverbios
    'siempre': 'tiempo', 'nunca': 'tiempo', 'también': 'modalidad',
    'tampoco': 'modalidad', 'aquí': 'espacio', 'allí': 'espacio',
    
    # Pronombres
    'yo': 'persona', 'tú': 'persona', 'él': 'persona', 'ella': 'persona',
    
    # Vivienda
    'casa': 'vivienda', 'hogar': 'vivienda', 'edificio': 'vivienda',
    
    # Profesión
    'profesión': 'profesión', 'trabajo': 'profesión',
    
    # Salud
    'salud': 'medicina', 'enfermedad': 'medicina',
    
    # Deporte
    'deporte': 'deporte',
    
    # Religión
    'fe': 'religión', 'religión': 'religión',
    
    # Filosofía
    'filosofía': 'filosofía', 'ética': 'filosofía', 'verdad': 'filosofía',
}


def main():
    print('=' * 60)
    print('ASIGNANDO CATEGORIAS SEMANTICAS')
    print('=' * 60)
    
    asignados = 0
    sin_categoria = []
    
    for t in Termino.objects.all():
        if t.categoria_semantica and t.categoria_semantica != 'general':
            continue
        
        palabra_lower = t.palabra.lower()
        if palabra_lower in CATEGORIAS:
            t.categoria_semantica = CATEGORIAS[palabra_lower]
            t.save()
            asignados += 1
        else:
            sin_categoria.append(t.palabra)
    
    print(f'Asignados: {asignados}')
    print(f'Sin categoria asignada: {len(sin_categoria)}')
    if sin_categoria:
        print('Palabras sin categoria:')
        for p in sin_categoria[:20]:
            print(f'  - {p}')
    
    # Resumen
    from collections import Counter
    cats = Counter(Termino.objects.values_list('categoria_semantica', flat=True))
    print()
    print('Categorias resultantes:')
    for cat, num in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {num}')
    print('=' * 60)


main()