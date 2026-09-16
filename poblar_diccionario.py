import os
import django

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lexicon_logic.settings')
django.setup()

from core.models import Termino

def poblar():
    datos = [
        {
            "palabra": "Chévere",
            "definicion": "Adjetivo usado para describir algo excelente, agradable o estupendo. Muy común en Colombia, Venezuela y Ecuador.",
            "categoria_gramatical": "ADJ"
        },
        {
            "palabra": "Bacán",
            "definicion": "Persona o cosa que es muy buena, atractiva o de excelente calidad. Se usa principalmente en Chile, Perú y Colombia.",
            "categoria_gramatical": "ADJ"
        },
        {
            "palabra": "Pibe",
            "definicion": "Forma coloquial de referirse a un niño, joven o muchacho. Es un término icónico del Cono Sur (Argentina y Uruguay).",
            "categoria_gramatical": "SUS"
        },
        {
            "palabra": "Chamo",
            "definicion": "Palabra para referirse a un niño o joven. Es la marca lingüística por excelencia de Venezuela.",
            "categoria_gramatical": "SUS"
        },
        {
            "palabra": "Chamba",
            "definicion": "Término coloquial para referirse al trabajo o empleo. Muy extendido en México, Centroamérica y Perú.",
            "categoria_gramatical": "SUS"
        },
        {
            "palabra": "Guagua",
            "definicion": "En el Cono Sur y países andinos significa 'bebé' o 'niño pequeño'. En el Caribe (Cuba, RD) se refiere a un autobús.",
            "categoria_gramatical": "SUS"
        }
    ]

    print("Iniciando la población de datos...")
    
    for item in datos:
        obj, created = Termino.objects.get_or_create(
            palabra=item['palabra'],
            defaults={
                'definicion': item['definicion'],
                'categoria_gramatical': item['categoria_gramatical']
            }
        )
        if created:
            print(f"✅ Agregado: {item['palabra']}")
        else:
            print(f"🟡 Ya existía: {item['palabra']}")

    print("--- Proceso finalizado ---")

if __name__ == "__main__":
    poblar()
