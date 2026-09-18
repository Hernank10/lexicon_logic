# ?? GU÷A DE PROGRAMACI‡N - 472 REGLAS PARA LEXICON LOGIC Y PROYECTOS DJANGO

**Documento:** Gu°a completa de reglas para estudio previo a revisi¢n de repositorios
**Proyecto base:** Lexicon Logic - Diccionario lexicogr†fico multilingÅe
**Versi¢n:** 1.0
**Fecha:** 17 de septiembre de 2026

---

## ÷NDICE

1. Introducci¢n
2. Bloque 1: Infraestructura i18n (Reglas 333-341)
3. Bloque 2: Entorno Python y antivirus (Reglas 342-395)
4. Bloque 3: Backups y scripts de respaldo (Reglas 396-429)
5. Bloque 4: Git y control de versiones (Reglas 430-472)
6. ApÇndice: Flujos de trabajo t°picos
7. ApÇndice: Errores comunes y soluciones

---

## INTRODUCCI‡N

Este documento recopila las 472 reglas aprendidas durante el desarrollo de Lexicon Logic, un diccionario lexicogr†fico multilingÅe construido con Django 5 y Python 3.12 en entorno Windows 10.

Las reglas est†n organizadas en 4 bloques tem†ticos y numeradas secuencialmente. Cada regla incluye:
- Contexto: cu†ndo aplica
- Regla: quÇ hacer
- Ejemplo: c¢digo concreto
- Por quÇ: raz¢n tÇcnica

Uso recomendado: leer los 4 bloques antes de empezar a revisar cualquier repositorio Django. Sirven como checklist mental.

---

## BLOQUE 1: INFRAESTRUCTURA I18N (Reglas 333-341)

### Regla 333 - Las 5 piezas de la infraestructura i18n

Contexto: Configurar internacionalizaci¢n en un proyecto Django.

Regla: La infraestructura i18n m°nima requiere 5 cosas:
1. USE_I18N = True en settings.py
2. LocaleMiddleware en MIDDLEWARE (despuÇs de SessionMiddleware)
3. LANGUAGES con los idiomas soportados
4. LOCALE_PATHS apuntando a locale/
5. Context processor con idiomas_disponibles e idioma_actual

Ejemplo:
```python
# settings.py
USE_I18N = True

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # despuÇs de sessions
]

LANGUAGES = [
    ('es', 'Espa§ol'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'core.context_processors.idiomas_disponibles',
]
```

Por quÇ: Sin estas 5 piezas, los templates no ven la lista de idiomas ni el idioma actual.

---

### Regla 334 - `{% trans %}` vs traducci¢n por ORM

Contexto: Traducir contenido en templates Django.

Regla: Para interfaz (botones, labels, mensajes) se usa `{% trans %}`. Para contenido del diccionario (palabras, definiciones) se usa el ORM:

```python
# En la vista
idioma_actual = request.session.get('idioma', 'es')
traduccion = termino.traducciones.filter(idioma__codigo=idioma_actual).first()
```

```html
{# En el template #}
{% if traduccion %}
  <p>{{ traduccion.traduccion }}</p>
{% endif %}
```

Por quÇ: `{% trans %}` usa archivos .po para textos est†ticos. El contenido del diccionario es din†mico (BD) y requiere consultas ORM.

---

### Regla 335 - El idioma viaja por `request.session`

Contexto: Persistir el idioma seleccionado.

Regla: El idioma_actual viaja por `request.session`, no por `request.user.profile`.

```python
request.session['idioma'] = 'en'
```

Por quÇ: El usuario puede cambiar de idioma sin modificar su perfil, y usuarios an¢nimos tambiÇn pueden usar el selector.

---

### Regla 336 - Bot¢n "Aportar traducci¢n" con query string

Contexto: Enlazar el bot¢n "Aportar traducci¢n" desde termino_detail.html.

Regla: El bot¢n pasa el idioma por query string para que el formulario se pre-rellene:

```html
<a href="{% url 'aportar_traduccion' termino.palabra %}?idioma={{ idioma_actual }}">
  ? Aportar traduccion en {{ idioma_actual }}
</a>
```

Por quÇ: El usuario llega al formulario con el idioma correcto ya seleccionado.

---

### Regla 337 - Selector con `onchange`

Contexto: Dropdown de idiomas en el navbar.

Regla: El selector usa `onchange="this.form.submit()"` para enviar el POST autom†ticamente:

```html
<form method="post" action="{% url 'cambiar_idioma' %}">
  {% csrf_token %}
  <select name="idioma" onchange="this.form.submit()">
    {% for lang in idiomas_disponibles %}
      <option value="{{ lang.codigo }}" {% if lang.codigo == idioma_actual %}selected{% endif %}>
        {{ lang.nombre_nativo }}
      </option>
    {% endfor %}
  </select>
</form>
```

Por quÇ: No requiere bot¢n adicional. UX m†s fluida.

---

### Regla 338 - `cambiar_idioma` redirige a `HTTP_REFERER`

Contexto: Vista cambiar_idioma.

Regla: Redirigir a HTTP_REFERER para que el usuario vuelva a la misma p†gina:

```python
def cambiar_idioma(request):
    if request.method == 'POST':
        request.session['idioma'] = request.POST.get('idioma', 'es')
    return redirect(request.META.get('HTTP_REFERER', '/'))
```

Por quÇ: El usuario cambia idioma desde /palabra/casa/ y quiere seguir ah°.

---

### Regla 339 - No mostrar traducci¢n si `idioma_actual == 'es'`

Contexto: Bloque de traducci¢n en termino_detail.html.

Regla: Si el idioma actual es espa§ol, no mostrar el bloque de traducci¢n.

```html
{% if idioma_actual != 'es' %}
  <div class="alert alert-info">
    {% if traduccion %}{{ traduccion.traduccion }}{% else %}Sin traducci¢n disponible{% endif %}
  </div>
{% endif %}
```

Por quÇ: El espa§ol es el idioma original del contenido.

---

### Regla 340 - Los archivos `.py` nunca deben tener BOM

Contexto: Crear archivos Python en Windows.

Regla: Los .py nunca deben tener BOM (\xef\xbb\xbf). Django 5 lanza SyntaxError.

Diagn¢stico:
```cmd
python -c "import os; [print(p) for p in [os.path.join(r,f) for r,_,fs in os.walk('.') for f in fs if f.endswith('.py')] if open(p,'rb').read(3)==b'\xef\xbb\xbf']"
```

Soluci¢n:
```python
open('archivo.py', 'w', encoding='utf-8').write(codigo)  # sin BOM
```

Por quÇ: Python 3.12+ detecta BOM y lanza SyntaxError.

---

### Regla 341 - Crear scripts sin BOM

Contexto: Escribir scripts .py desde CMD o Notepad.

Regla: Para crear scripts sin BOM:
- Opci¢n 1: open(..., 'w', encoding='utf-8') desde Python
- Opci¢n 2: Notepad 