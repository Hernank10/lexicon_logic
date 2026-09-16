import re
import os

BASE = r"E:\02_proyectos\lexicon_logic\_original"

with open(os.path.join(BASE, "strings.txt"), encoding="utf-8") as f:
    STRINGS = [line.strip() for line in f if line.strip()]

print("Strings cargadas:", len(STRINGS))


def marcar_archivo(ruta, strings):
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as f:
        c = f.read()
    if "{% load i18n %}" not in c:
        lineas = c.split(chr(10))
        if len(lineas) > 0 and lineas[0].startswith("{% extends"):
            lineas.insert(1, "{% load i18n %}")
        else:
            lineas.insert(0, "{% load i18n %}")
        c = chr(10).join(lineas)
    cambios = 0
    for s in strings:
        marca = "{% trans \"" + s + "\" %}"
        if marca in c:
            continue
        s_esc = re.escape(s)
        patron = r"^>^(\s*^)" + s_esc + r"^(\s*^)^<"
        reemplazo = r"^>\g^<1^>" + marca + r"\g^<2^>^<"
        if re.search(patron, c):
            c = re.sub(patron, reemplazo, c, count=1)
            cambios += 1
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(c)
    return cambios


ARCHIVOS = [
    r"core\templates\core\index.html",
    r"templates\base.html",
    r"templates\registration\login.html",
    r"templates\registration\registro.html",
    r"templates\perfil.html",
    r"cursos\templates\cursos\lista_cursos.html",
    r"cursos\templates\cursos\detalle_curso.html",
    r"cursos\templates\cursos\detalle_leccion.html",
    r"cursos\templates\cursos\dashboard.html",
    r"cursos\templates\cursos\certificado.html",
]

print("=" * 60)
print("MARCANDO STRINGS")
print("=" * 60)
total = 0
for rel in ARCHIVOS:
    ruta = os.path.join(BASE, rel)
    cambios = marcar_archivo(ruta, STRINGS)
    print("  " + rel + ": " + str(cambios) + " marcadas")
    total += cambios
print()
print("Total marcadas: " + str(total))
