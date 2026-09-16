"""
Añade los modelos Idioma y TraduccionTermino a core/models.py
"""
from pathlib import Path

RUTA = Path(r'E:\02_proyectos\lexicon_logic\_original\core\models.py')

MODELOS_NUEVOS = """


# ============================================================
# MODELOS DE INTERNACIONALIZACION (i18n)
# ============================================================

class Idioma(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre_nativo = models.CharField(max_length=100)
    nombre_ingles = models.CharField(max_length=100)
    familia = models.CharField(max_length=50, blank=True)
    hablantes_millones = models.IntegerField(default=0)
    DIRECCION_CHOICES = [
        ('ltr', 'Izquierda a derecha'),
        ('rtl', 'Derecha a izquierda'),
    ]
    direccion = models.CharField(max_length=3, choices=DIRECCION_CHOICES, default='ltr')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['-hablantes_millones']
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    def __str__(self):
        return self.nombre_nativo + ' (' + self.codigo + ')'


class TraduccionTermino(models.Model):
    CORRESPONDENCIA_CHOICES = [
        ('exacta', 'Traduccion exacta'),
        ('parcial', 'Parcial'),
        ('aproximada', 'Aproximada'),
        ('cultural', 'Equivalente cultural'),
    ]

    termino = models.ForeignKey(Termino, on_delete=models.CASCADE, related_name='traducciones')
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE, related_name='traducciones')
    traduccion = models.CharField(max_length=200)
    definicion_nativa = models.TextField(blank=True)
    ejemplo_nativo = models.TextField(blank=True)
    notas = models.TextField(blank=True)
    nivel_correspondencia = models.CharField(max_length=20, choices=CORRESPONDENCIA_CHOICES, default='exacta')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='traducciones_aportadas')
    verificado = models.BooleanField(default=False)
    votos = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('termino', 'idioma')
        ordering = ['-votos']
        verbose_name = 'Traduccion de termino'
        verbose_name_plural = 'Traducciones de terminos'

    def __str__(self):
        return self.termino.palabra + ' -> ' + self.traduccion + ' (' + self.idioma.codigo + ')'
"""

# Leer el archivo actual
content = RUTA.read_text(encoding='utf-8')

if 'class Idioma' in content:
    print('AVISO: Idioma ya existe en models.py')
else:
    content += MODELOS_NUEVOS
    RUTA.write_text(content, encoding='utf-8')
    print('OK - modelos anadidos a core/models.py')