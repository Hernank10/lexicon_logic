# fix_i18n.py
import os, re

BASE = r"E:\02_proyectos\lexicon_logic\_original"

# ─── 1) VIEWS.PY ───────────────────────────────────────
views_path = os.path.join(BASE, "core", "views.py")
c = open(views_path, encoding="utf-8").read()

nueva_vista = '''def termino_detail(request, slug):
    """Mini vista de una palabra con todos sus campos lexicograficos."""
    termino = get_object_or_404(Termino, palabra__iexact=slug)
    variantes = termino.variantes.all().order_by('pais')

    if termino.categoria_semantica:
        relacionados = Termino.objects.filter(
            categoria_semantica=termino.categoria_semantica
        ).exclude(id=termino.id)[:6]
    else:
        relacionados = Termino.objects.none()

    idioma_actual = request.session.get('idioma', 'es')
    traduccion = None
    if idioma_actual and idioma_actual != 'es':
        traduccion = termino.traducciones.filter(
            idioma__codigo=idioma_actual
        ).first()

    return render(request, 'core/termino_detail.html', {
        'termino': termino,
        'variantes': variantes,
        'relacionados': relacionados,
        'idioma_actual': idioma_actual,
        'traduccion': traduccion,
    })


def cambiar_idioma(request):
    """Guarda el idioma seleccionado en la sesion y redirige atras."""
    if request.method == 'POST':
        idioma = request.POST.get('idioma', 'es')
        request.session['idioma'] = idioma
    return redirect(request.META.get('HTTP_REFERER', '/'))
'''

# Reemplazar la funcion termino_detail existente
patron = re.compile(r"def termino_detail\(request, slug\):.*?(?=\n\n\n# ═|\ndef |\Z)", re.DOTALL)
if patron.search(c):
    c = patron.sub(nueva_vista, c, count=1)
    print("[OK] termino_detail reemplazada")
else:
    print("[WARN] No se encontro patron termino_detail, anadiendo al final")
    c += "\n\n" + nueva_vista

# Anadir cambiar_idioma si no existe
if "def cambiar_idioma" not in c:
    c += "\n\n" + nueva_vista.split("def cambiar_idioma")[1].join(["def cambiar_idioma", ""])
    print("[OK] cambiar_idioma anadida")

open(views_path, "w", encoding="utf-8").write(c)
print("[OK] views.py guardado")

# ─── 2) URLS.PY ────────────────────────────────────────
urls_path = os.path.join(BASE, "lexicon_logic", "urls.py")
u = open(urls_path, encoding="utf-8").read()

if "cambiar_idioma" not in u:
    if "from core import views" not in u:
        u = u.replace("from django.urls import path", "from django.urls import path\nfrom core import views as core_views")
    u = u.replace("urlpatterns = [", "urlpatterns = [\n    path('cambiar-idioma/', core_views.cambiar_idioma, name='cambiar_idioma'),")
    open(urls_path, "w", encoding="utf-8").write(u)
    print("[OK] urls.py actualizado")
else:
    print("[INFO] urls.py ya tenia cambiar_idioma")

# ─── 3) TEMPLATE ───────────────────────────────────────
tpl = '''<!DOCTYPE html>
<html lang="{{ idioma_actual|default:'es' }}">
<head>
<meta charset="UTF-8">
<title>{{ termino.palabra }} | Lexicon Logic</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-dark">
<div class="container d-flex justify-content-between">
<a class="navbar-brand" href="/">LEXICON LOGIC</a>
<form method="post" action="{% url 'cambiar_idioma' %}" class="d-flex align-items-center gap-2">
  {% csrf_token %}
  <select name="idioma" class="form-select form-select-sm" style="width:auto;" onchange="this.form.submit()">
    {% for lang in idiomas_disponibles %}
      <option value="{{ lang.codigo }}" {% if lang.codigo == idioma_actual %}selected{% endif %}>
        {{ lang.nombre_nativo|default:lang.nombre }}
      </option>
    {% endfor %}
  </select>
</form>
</div>
</nav>

<div class="container mt-4">
<a href="{% url 'home' %}" class="btn btn-sm btn-outline-secondary mb-3">Volver</a>

<div class="card shadow-sm mb-4">
<div class="card-body">
<h1>{{ termino.palabra }}</h1>
<span class="badge bg-primary">{{ termino.get_categoria_gramatical_display }}</span>
{% if termino.nivel %}<span class="badge bg-info">{{ termino.get_nivel_display }}</span>{% endif %}
{% if termino.frecuencia %}<span class="badge bg-warning">{{ termino.get_frecuencia_display }}</span>{% endif %}
{% if termino.dificultad %}<span class="badge bg-secondary">{{ termino.get_dificultad_display }}</span>{% endif %}
<hr>

{% if idioma_actual != 'es' %}
  <div class="alert alert-info">
    <h5 class="mb-1">
      {% if traduccion %}{{ traduccion.traduccion }}{% else %}<em>Sin traduccion disponible en este idioma</em>{% endif %}
    </h5>
    {% if traduccion and traduccion.notas %}<small>{{ traduccion.notas }}</small>{% endif %}
  </div>
{% endif %}

<h4>Definicion</h4>
<p>{{ termino.definicion }}</p>
{% if termino.acepciones %}<h4>Acepciones</h4><ul>{% for a in termino.acepciones %}<li>{{ a }}</li>{% endfor %}</ul>{% endif %}
{% if termino.ejemplo %}<h4>Ejemplo</h4><blockquote class="blockquote bg-light p-3 border-start border-4 border-primary">{{ termino.ejemplo }}</blockquote>{% endif %}
{% if termino.etimologia %}<h4>Etimologia</h4><p><em>{{ termino.etimologia }}</em></p>{% endif %}
{% if termino.sinonimos %}<h4>Sinonimos</h4><ul>{% for s in termino.sinonimos %}<li>{{ s }}</li>{% endfor %}</ul>{% endif %}
{% if termino.antonimos %}<h4>Antonimos</h4><ul>{% for a in termino.antonimos %}<li>{{ a }}</li>{% endfor %}</ul>{% endif %}
{% if termino.familia_lexica %}<h4>Familia lexica</h4><ul>{% for f in termino.familia_lexica %}<li>{{ f }}</li>{% endfor %}</ul>{% endif %}
{% if termino.locuciones %}<h4>Locuciones</h4><ul>{% for l in termino.locuciones %}<li>{{ l }}</li>{% endfor %}</ul>{% endif %}
{% if termino.categoria_semantica %}<p><strong>Categoria semantica:</strong> {{ termino.categoria_semantica }}</p>{% endif %}
{% if termino.marcas %}<p><strong>Marcas:</strong> {% for m in termino.marcas %}<span class="badge bg-secondary">{{ m }}</span> {% endfor %}</p>{% endif %}
</div>
</div>

{% if idioma_actual != 'es' %}
<div class="mb-4">
  <a href="{% url 'aportar_traduccion' termino.palabra %}?idioma={{ idioma_actual }}" class="btn btn-outline-primary btn-sm">
    ➕ Aportar traduccion en {{ idioma_actual }}
  </a>
</div>
{% endif %}

{% if variantes %}
<div class="card shadow-sm mb-4"><div class="card-body">
<h4>Variantes regionales</h4>
<table class="table"><thead><tr><th>Pais</th><th>Variante</th><th>Frecuencia</th></tr></thead>
<tbody>{% for v in variantes %}<tr><td>{{ v.pais }}</td><td>{{ v.palabra_variante }}</td><td>{{ v.frecuencia_uso }}/10</td></tr>{% endfor %}</tbody>
</table></div></div>
{% endif %}

{% if relacionados %}
<div class="card shadow-sm"><div class="card-body">
<h4>Terminos relacionados</h4>
<ul>{% for r in relacionados %}<li><a href="{% url 'termino_detail' r.palabra %}">{{ r.palabra }}</a></li>{% endfor %}</ul>
</div></div>
{% endif %}
</div>
</body>
</html>'''

tpl_path = os.path.join(BASE, "core", "templates", "core", "termino_detail.html")
open(tpl_path, "w", encoding="utf-8").write(tpl)
print("[OK] termino_detail.html guardado")

print("\n✅ Listo. Ahora ejecuta: E:\\PythonPortable_Django5\\python.exe manage.py check")