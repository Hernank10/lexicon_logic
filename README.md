# create_readme.py
BASE = r'E:\02_proyectos\lexicon_logic\_original'

readme = '''# Lexicon Logic

Diccionario lexicografico multilingue colaborativo.

Lexicon Logic es una plataforma web construida con Django 5 que permite consultar terminos en castellano, ver sus definiciones, variantes regionales y traducciones en 30 idiomas. Los usuarios registrados pueden aportar nuevas traducciones.

---

## Caracteristicas

- 30 idiomas soportados (espanol, ingles, frances, portugues, chino, arabe, etc.)
- Definiciones completas con categoria gramatical, nivel, frecuencia y dificultad
- Variantes regionales de 20+ paises hispanohablantes
- Traducciones colaborativas aportadas por usuarios
- Selector de idioma en el navbar con auto-submit
- Autenticacion con login, logout y registro
- Diseno responsive con Bootstrap 5
- Internacionalizacion (i18n) con trans y ORM

---

## Arquitectura

### Apps Django
## Arquitectura

### Apps Django
lexicon_logic/
├── core/ → App principal
│ ├── models.py → Termino, Variante, Idioma, TraduccionTermino
│ ├── views.py → home, termino_detail, cambiar_idioma, aportar_traduccion
│ ├── forms.py → TerminoForm, TraduccionForm
│ ├── urls.py → URLs de la app
│ └── templates/core/ → index.html, termino_detail.html, aportar_traduccion.html
├── lexicon_logic/ → Configuracion del proyecto
│ ├── settings.py → Configuracion (i18n, middleware, templates)
│ └── urls.py → URLs raiz
├── templates/ → Templates globales
│ ├── perfil.html
│ └── registration/
│ ├── login.html
│ └── registro.html
└── locale/ → Traducciones (10 idiomas)

text

### Modelos principales

| Modelo | Descripcion |
|--------|-------------|
| Termino | Palabra + definicion + categoria gramatical + nivel + frecuencia + dificultad + etimologia + sinonimos + antonimos + familia lexica + locuciones |
| Variante | Variante regional por pais con frecuencia de uso |
| Idioma | 30 idiomas con codigo, nombre nativo, familia, hablantes, direccion |
| TraduccionTermino | Traduccion de un termino a otro idioma con nivel de correspondencia |

---

## Instalacion

### Requisitos

- Python 3.12+
- Django 5.2+
- SQLite (incluido)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hernank10/lexicon_logic.git
cd lexicon_logic

# 2. Crear entorno virtual (opcional)
python -m venv venv
venv\\Scripts\\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install django

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Cargar datos de prueba (opcional)
python crear_datos_prueba.py

# 7. Arrancar servidor
python manage.py runserver
Abrir en el navegador: http://127.0.0.1:8000/

Uso
URLs principales
URL	Descripcion
/	Home con buscador
/palabra/<slug>/	Detalle de un termino
/palabra/<slug>/aportar-traduccion/	Aportar traduccion
/accounts/login/	Login
/accounts/logout/	Logout
/accounts/registro/	Registro
/perfil/	Perfil del usuario
/admin/	Admin de Django
Flujo de usuario
text
1. Abre / → Home con buscador
2. Busca un termino (ej: "casa")
3. Clic en el termino → Detalle
4. Cambia el idioma en el dropdown → Se recarga
5. Si existe traduccion → Se muestra en un recuadro
6. Clic en "Aportar traduccion" → Formulario
7. Rellena y envia → Se guarda (autor = usuario)
8. Redirige al termino → Aparece la traduccion
Idiomas soportados
Codigo	Idioma	Nombre nativo
es	Espanol	Espanol
en	Ingles	English
zh-hans	Chino	中文
hi	Hindi	हिन्दी
ar	Arabe	العربية
fr	Frances	Francais
pt	Portugues	Portugues
ru	Ruso	Русский
bn	Bengali	বাংলা
ur	Urdu	اردو
Scripts de prueba
Script	Funcion
crear_datos_prueba.py	Crea terminos de prueba
crear_idiomas.py	Crea los 30 idiomas
cargar_traducciones_prueba.py	Carga traducciones de prueba
poblar_diccionario.py	Puebla el diccionario
poblar_usuarios_total.py	Crea usuarios de prueba
marcar_trans.py	Marca cadenas traducibles
add_i18n.py	Anade i18n al proyecto
fix_i18n.py	Corrige i18n
backup.ps1	Backup automatico
Tecnologias
Capa	Tecnologia
Backend	Django 5.2.11, Python 3.12.4
Base de datos	SQLite
Frontend	Bootstrap 5.3
i18n	django.utils.translation
Auth	django.contrib.auth
Admin	django.contrib.admin
Estructura de templates
text
core/templates/core/
├── index.html              → Home con buscador
├── termino_detail.html     → Detalle de termino
└── aportar_traduccion.html → Formulario de traduccion

templates/
├── perfil.html             → Perfil del usuario
└── registration/
    ├── login.html          → Login
    └── registro.html       → Registro
Comandos utiles
bash
# Verificar el proyecto
python manage.py check

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Arrancar servidor en puerto especifico
python manage.py runserver 127.0.0.1:8016
Estado del proyecto
Componente	Estado
i18n (30 idiomas)	OK
Traducciones en termino_detail	OK
Vista aportar_traduccion	OK
Login/logout	OK
Registro	OK
Perfil	OK
Admin	OK
Selector de idioma	OK
Home publico	OK
Contribuir
Fork el repositorio

Crea una rama (git checkout -b feature/nueva-funcionalidad)

Commit tus cambios (git commit -m 'feat: nueva funcionalidad')

Push a la rama (git push origin feature/nueva-funcionalidad)

Abre un Pull Request

Licencia
MIT

Autor
Hernank10 - https://github.com/Hernank10

