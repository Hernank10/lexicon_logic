from django.db import models

class Termino(models.Model):
    """
    Representa la palabra base o concepto original.
    """
    palabra = models.CharField(max_length=100, unique=True, verbose_name="Palabra Base")
    definicion = models.TextField(blank=True, verbose_name="Definición General")
    categoria_gramatical = models.CharField(
        max_length=20, 
        choices=[
            ('sustantivo', 'Sustantivo'),
            ('verbo', 'Verbo'),
            ('adjetivo', 'Adjetivo'),
        ],
        default='sustantivo'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Término"
        verbose_name_plural = "Términos"

    def __str__(self):
        return self.palabra

class Variante(models.Model):
    """
    Almacena las variantes léxicas (geográficas, sociales, etc.) 
    adaptadas de tus scripts previos.
    """
    termino_base = models.ForeignKey(Termino, on_delete=models.CASCADE, related_name='variantes')
    palabra_variante = models.CharField(max_length=100, verbose_name="Variante")
    pais = models.CharField(max_length=50, verbose_name="País/Región")
    explicacion = models.TextField(blank=True, verbose_name="Contexto de uso")
    frecuencia_uso = models.IntegerField(default=1, help_text="Escala de popularidad (1-10)")

    class Meta:
        verbose_name = "Variante Léxica"
        verbose_name_plural = "Variantes Léxicas"

    def __str__(self):
        return f"{self.palabra_variante} ({self.pais})"
