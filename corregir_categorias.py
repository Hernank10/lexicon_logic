"""
Corrige las categorÃÂ­as semÃÂ¡nticas rotas y regenera los cursos.
"""
from core.models import Termino
from cursos.models import Curso, Leccion, Ejercicio


# Mapa de correcciones: categorÃÂ­a rota -> categorÃÂ­a correcta
CORRECCIONES = {
    'acci\ufffdn': 'acciÃÂ³n',
    'astronom\ufffda': 'astronomÃÂ­a',
    'biolog\ufffda': 'biologÃÂ­a',
    'cognici\ufffdn': 'cogniciÃÂ³n',
    'comunicaci\ufffdn': 'comunicaciÃÂ³n',
    'cosmolog\ufffda': 'cosmologÃÂ­a',
    'econom\ufffda': 'economÃÂ­a',
    'educaci\ufffdn': 'educaciÃÂ³n',
    'emoci\ufffdn': 'emociÃÂ³n',
    'epistemolog\ufffda': 'epistemologÃÂ­a',
    'filosof\ufffda': 'filosofÃÂ­a',
    'f\ufffdsica': 'fÃÂ­sica',
    'geograf\ufffda': 'geografÃÂ­a',
    'gram\ufffdtica': 'gramÃÂ¡tica',
    'ling\ufffd\ufffdstica': 'lingÃÂ¼ÃÂ­stica',
    'literatur\ufffda': 'literatura',
    'matem\ufffdticas': 'matemÃÂ¡ticas',
    'percepci\ufffdn': 'percepciÃÂ³n',
    'pol\ufffdtica': 'polÃÂ­tica',
    'profesi\ufffdn': 'profesiÃÂ³n',
    'psicolog\ufffda': 'psicologÃÂ­a',
    'relaci\ufffdn': 'relaciÃÂ³n',
    'religi\ufffdn': 'religiÃÂ³n',
    'valoraci\ufffdn': 'valoraciÃÂ³n',
    # GenÃÂ©ricas
    'educacion': 'educaciÃÂ³n',
    'musica': 'mÃÂºsica',
    'medico': 'mÃÂ©dico',
    'matematicas': 'matemÃÂ¡ticas',
    'geografia': 'geografÃÂ­a',
    'filosofia': 'filosofÃÂ­a',
}


def corregir_categoria(categoria):
    """Corrige una categorÃÂ­a rota."""
    if not categoria:
        return categoria
    
    # Reemplazo exacto
    if categoria in CORRECCIONES:
        return CORRECCIONES[categoria]
    
    # Reemplazo por patrÃÂ³n (para las no listadas)
    # Patrones comunes:
    reemplazos_patron = [
        ('aci\ufffdn', 'aciÃÂ³n'),
        ('ici\ufffdn', 'iciÃÂ³n'),
        ('i\ufffdn', 'iÃÂ³n'),
        ('olog\ufffda', 'ologÃÂ­a'),
        ('nom\ufffda', 'nomÃÂ­a'),
        ('graf\ufffda', 'grafÃÂ­a'),
        ('f\ufffdsica', 'fÃÂ­sica'),
        ('matem\ufffdticas', 'matemÃÂ¡ticas'),
        ('ling\ufffd\ufffdstica', 'lingÃÂ¼ÃÂ­stica'),
        ('pol\ufffdtica', 'polÃÂ­tica'),
        ('pr\ufffdctica', 'prÃÂ¡ctica'),
        ('psicolog\ufffda', 'psicologÃÂ­a'),
    ]
    
    for patron, correcto in reemplazos_patron:
        if patron in categoria:
            return categoria.replace(patron, correcto)
    
    return categoria


def main():
    print('=' * 60)
    print('CORRIGIENDO CATEGORIAS SEMANTICAS')
    print('=' * 60)
    
    total = 0
    corregidos = 0
    categorias_unicas = set()
    
    for t in Termino.objects.all():
        total += 1
        original = t.categoria_semantica
        
        if '\ufffd' in original or any(c in original for c in ['educacion', 'musica', 'medico']):
            nueva = corregir_categoria(original)
            if nueva != original:
                t.categoria_semantica = nueva
                t.save()
                corregidos += 1
                categorias_unicas.add(nueva)
                print(f'  {repr(original)} -> {repr(nueva)}')
    
    print()
    print(f'Terminos totales: {total}')
    print(f'Corregidos: {corregidos}')
    print(f'Categorias unicas corregidas: {len(categorias_unicas)}')
    print()
    print('Categorias resultantes:')
    for c in sorted(categorias_unicas):
        print(f'  - {c}')
    print('=' * 60)


main()