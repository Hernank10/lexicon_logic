from core.models import Idioma

IDIOMAS = [
    ("zh-hans", u"\u4e2d\u6587", "Chinese (Simplified)", "Sino-tibetana", 1100, "ltr"),
    ("en", "English", "English", "Germanica", 380, "ltr"),
    ("hi", u"\u0939\u093f\u0928\u094d\u0926\u0940", "Hindi", "Indoeuropea", 345, "ltr"),
    ("es", u"Espa\u00f1ol", "Spanish", "Romance", 485, "ltr"),
    ("ar", u"\u0627\u0644\u0639\u0631\u0628\u064a\u0629", "Arabic", "Semitica", 280, "rtl"),
    ("bn", u"\u09ac\u09be\u0982\u09b2\u09be", "Bengali", "Indoeuropea", 275, "ltr"),
    ("pt", u"Portugu\u00eas", "Portuguese", "Romance", 260, "ltr"),
    ("ru", u"\u0420\u0443\u0441\u0441\u043a\u0438\u0439", "Russian", "Eslava", 255, "ltr"),
    ("ja", u"\u65e5\u672c\u8a9e", "Japanese", "Japonica", 125, "ltr"),
    ("de", "Deutsch", "German", "Germanica", 135, "ltr"),
    ("fr", u"Fran\u00e7ais", "French", "Romance", 280, "ltr"),
    ("id", "Bahasa Indonesia", "Indonesian", "Austronesia", 200, "ltr"),
    ("ur", u"\u0627\u0631\u062f\u0648", "Urdu", "Indoeuropea", 230, "rtl"),
    ("sw", "Kiswahili", "Swahili", "Niger-congo", 200, "ltr"),
    ("tr", u"T\u00fcrk\u00e7e", "Turkish", "Turquica", 90, "ltr"),
    ("ta", u"\u0ba4\u0bae\u0bbf\u0bb4\u0bcd", "Tamil", "Dravidica", 85, "ltr"),
    ("vi", u"Ti\u1ebfng Vi\u1ec7t", "Vietnamese", "Austroasiatica", 85, "ltr"),
    ("ko", u"\ud55c\uad6d\uc5b4", "Korean", "Coreanica", 80, "ltr"),
    ("it", "Italiano", "Italian", "Romance", 65, "ltr"),
    ("th", u"\u0e44\u0e17\u0e22", "Thai", "Tai-kadai", 60, "ltr"),
    ("gu", u"\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0", "Gujarati", "Indoeuropea", 55, "ltr"),
    ("fa", u"\u0641\u0627\u0631\u0633\u06cc", "Persian", "Indoeuropea", 110, "rtl"),
    ("pl", "Polski", "Polish", "Eslava", 40, "ltr"),
    ("uk", u"\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430", "Ukrainian", "Eslava", 40, "ltr"),
    ("ms", "Bahasa Melayu", "Malay", "Austronesia", 35, "ltr"),
    ("te", u"\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41", "Telugu", "Dravidica", 95, "ltr"),
    ("mr", u"\u092e\u0930\u093e\u0920\u0940", "Marathi", "Indoeuropea", 85, "ltr"),
    ("he", u"\u05e2\u05d1\u05e8\u05d9\u05ea", "Hebrew", "Semitica", 9, "rtl"),
    ("nl", "Nederlands", "Dutch", "Germanica", 25, "ltr"),
    ("fil", "Filipino", "Filipino", "Austronesia", 45, "ltr"),
]

creados = 0
existentes = 0
for i, (codigo, nativo, ingles, familia, millones, direccion) in enumerate(IDIOMAS):
    obj, created = Idioma.objects.get_or_create(
        codigo=codigo,
        defaults={
            "nombre_nativo": nativo,
            "nombre_ingles": ingles,
            "familia": familia,
            "hablantes_millones": millones,
            "direccion": direccion,
            "orden": i,
        }
    )
    if created:
        creados += 1
    else:
        existentes += 1

print("Idiomas creados:", creados)
print("Ya existian:", existentes)
print("Total en BD:", Idioma.objects.count())