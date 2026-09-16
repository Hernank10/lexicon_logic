from core.models import Termino

ULTIMAS = {
    'pajaro': 'naturaleza',
    'gato': 'naturaleza',
    'perro': 'naturaleza',
    'animal': 'naturaleza',
    'flor': 'naturaleza',
    'arbol': 'naturaleza',
    'rio': 'naturaleza',
    'montana': 'naturaleza',
    'naturaleza': 'naturaleza',
    'mundo': 'existencia',
    'musica': 'arte',
    'historia': 'humanidades',
    'educacion': 'educacion',
    'agua': 'naturaleza',
}

def limpiar(p):
    p = p.lower().strip()
    for c, r in [(chr(225),'a'),(chr(233),'e'),(chr(237),'i'),(chr(243),'o'),(chr(250),'u'),(chr(241),'n')]:
        p = p.replace(c, r)
    return p

asignados = 0
for t in Termino.objects.filter(categoria_semantica=''):
    p = limpiar(t.palabra)
    if p in ULTIMAS:
        t.categoria_semantica = ULTIMAS[p]
        t.save()
        asignados += 1
        print(f'  {t.palabra} -> {ULTIMAS[p]}')

print(f'Total asignados: {asignados}')
print(f'Sin categoria: {Termino.objects.filter(categoria_semantica="").count()}')

from collections import Counter
cats = Counter(Termino.objects.values_list('categoria_semantica', flat=True))
print()
print('Categorias finales:')
for cat, num in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {num}')
