"""
Carga las palabras del JSON lexicográfico a la BD.
Con el modelo ampliado, carga TODOS los campos disponibles.
"""
import json
from pathlib import Path
from core.models import Termino, Variante


def cargar_json(json_path='palabras_lexicograficas.json'):
    ruta = Path(json_path)
    if not ruta.exists():
        print(f'❌ No existe: {ruta.absolute()}')
        return

    with open(ruta, encoding='utf-8') as f:
        data = json.load(f)

    print(f'📄 {data["meta"]["titulo"]}')
    print(f'📊 Total en JSON: {len(data["entradas"])}')
    print()

    # Mapeo JSON -> modelo
    MAPA = {
        'lema': 'palabra',
        'categoria_gramatical': 'categoria_gramatical',
        'definicion': 'definicion',
        'acepciones': 'acepciones',
        'etimologia': 'etimologia',
        'ejemplo': 'ejemplo',
        'sinonimos': 'sinonimos',
        'antonimos': 'antonimos',
        'familia_lexica': 'familia_lexica',
        'locuciones': 'locuciones',
        'nivel': 'nivel',
        'frecuencia': 'frecuencia',
        'marcas': 'marcas',
        'categoria_semantica': 'categoria_semantica',
        'dificultad': 'dificultad',
    }

    creados = 0
    existentes = 0
    errores = 0
    variantes_creadas = 0

    # Normalizar categorías a las del modelo
    normalizar = {
        'SUSTANTIVO': 'sustantivo', 'sustantivo': 'sustantivo',
        'VERBO': 'verbo', 'verbo': 'verbo',
        'ADJETIVO': 'adjetivo', 'adjetivo': 'adjetivo',
        'ADVERBIO': 'adverbio', 'adverbio': 'adverbio',
        'PRONOMBRE': 'pronombre', 'pronombre': 'pronombre',
        'PREPOSICION': 'preposicion', 'preposicion': 'preposicion',
        'CONJUNCION': 'conjuncion', 'conjuncion': 'conjuncion',
        'INTERJECCION': 'interjeccion', 'interjeccion': 'interjeccion',
        'ARTICULO': 'articulo', 'articulo': 'articulo',
    }

    for entrada in data['entradas']:
        palabra = entrada['lema']
        try:
            defaults = {}
            for campo_json, campo_modelo in MAPA.items():
                if campo_json in entrada and campo_json != 'lema':
                    valor = entrada[campo_json]
                    if valor is None:
                        continue
                    # Normalizar categoría
                    if campo_modelo == 'categoria_gramatical':
                        valor = normalizar.get(valor, 'sustantivo')
                    # Normalizar nivel/dificultad (quitar tildes)
                    if campo_modelo == 'nivel':
                        valor = valor.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                    if campo_modelo == 'dificultad':
                        valor = valor.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                    defaults[campo_modelo] = valor

            obj, created = Termino.objects.get_or_create(
                palabra=palabra,
                defaults=defaults
            )
            if created:
                creados += 1
            else:
                existentes += 1

            # Variantes regionales
            for var in entrada.get('variantes_regionales', []):
                _, v_created = Variante.objects.get_or_create(
                    termino_base=obj,
                    pais=var['pais'],
                    palabra_variante=var['forma'],
                )
                if v_created:
                    variantes_creadas += 1

        except Exception as e:
            errores += 1
            print(f'  ❌ "{palabra}": {e}')

    print()
    print('=' * 50)
    print(f'✅ Creados:      {creados}')
    print(f'⏭️  Ya existian: {existentes}')
    print(f'🔀 Variantes:    {variantes_creadas}')
    print(f'❌ Errores:      {errores}')
    print(f'📊 Terminos BD:  {Termino.objects.count()}')
    print(f'📊 Variantes BD: {Variante.objects.count()}')
    print('=' * 50)


cargar_json()