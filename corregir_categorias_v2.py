from core.models import Termino

CORRECCIONES = {
    'acci\ufffdn': 'acción',
    'astronom\ufffda': 'astronomía',
    'biolog\ufffda': 'biología',
    'cognici\ufffdn': 'cognición',
    'comunicaci\ufffdn': 'comunicación',
    'cosmolog\ufffda': 'cosmología',
    'econom\ufffda': 'economía',
    'educaci\ufffdn': 'educación',
    'emoci\ufffdn': 'emoción',
    'epistemolog\ufffda': 'epistemología',
    'filosof\ufffda': 'filosofía',
    'f\ufffdsica': 'física',
    'geograf\ufffda': 'geografía',
    'gram\ufffdtica': 'gramática',
    'ling\ufffd\ufffdstica': 'lingüística',
    'matem\ufffdticas': 'matemáticas',
    'percepci\ufffdn': 'percepción',
    'pol\ufffdtica': 'política',
    'profesi\ufffdn': 'profesión',
    'psicolog\ufffda': 'psicología',
    'relaci\ufffdn': 'relación',
    'religi\ufffdn': 'religión',
    'valoraci\ufffdn': 'valoración',
}

def corregir(cat):
    if cat in CORRECCIONES:
        return CORRECCIONES[cat]
    for viejo, nuevo in CORRECCIONES.items():
        if viejo in cat:
            return cat.replace(viejo, nuevo)
    return cat

for t in Termino.objects.all():
    orig = t.categoria_semantica
    if orig and '\ufffd' in orig:
        t.categoria_semantica = corregir(orig)
        t.save()
        print(f'  {repr(orig)} -> {repr(t.categoria_semantica)}')

print(f'Total: {Termino.objects.count()}')