from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Termino(models.Model):
    CATEGORIA_GRAMATICAL_CHOICES = [
        ('sustantivo', 'Sustantivo'),
        ('verbo', 'Verbo'),
        ('adjetivo', 'Adjetivo'),
        ('adverbio', 'Adverbio'),
        ('pronombre', 'Pronombre'),
        ('preposicion', 'Preposicion'),
        ('conjuncion', 'Conjuncion'),
        ('interjeccion', 'Interjeccion'),
        ('articulo', 'Articulo'),
    ]
    NIVEL_CHOICES = [
        ('formal', 'Formal'),
        ('coloquial', 'Coloquial'),
        ('culto', 'Culto'),
        ('tecnico', 'Tecnico'),
        ('literario', 'Literario'),
        ('juvenil', 'Juvenil'),
    ]
    FRECUENCIA_CHOICES = [
        ('muy alta', 'Muy alta'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('muy baja', 'Muy baja'),
    ]
    DIFICULTAD_CHOICES = [
        ('basico', 'Basico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    palabra = models.CharField(max_length=100, unique=True, verbose_name='Palabra Base')
    definicion = models.TextField(blank=True, verbose_name='Definicion General')
    categoria_gramatical = models.CharField(max_length=20, choices=CATEGORIA_GRAMATICAL_CHOICES, default='sustantivo')
    acepciones = models.JSONField(default=list, blank=True, verbose_name='Acepciones')
    etimologia = models.TextField(blank=True, verbose_name='Etimologia')
    ejemplo = models.TextField(blank=True, verbose_name='Ejemplo de uso')
    sinonimos = models.JSONField(default=list, blank=True, verbose_name='Sinonimos')
    antonimos = models.JSONField(default=list, blank=True, verbose_name='Antonimos')
    familia_lexica = models.JSONField(default=list, blank=True, verbose_name='Familia lexica')
    locuciones = models.JSONField(default=list, blank=True, verbose_name='Locuciones')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, blank=True, verbose_name='Nivel de uso')
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, blank=True, verbose_name='Frecuencia')
    marcas = models.JSONField(default=list, blank=True, verbose_name='Marcas de uso')
    categoria_semantica = models.CharField(max_length=50, blank=True, verbose_name='Categoria semantica')
    dificultad = models.CharField(max_length=20, choices=DIFICULTAD_CHOICES, blank=True, verbose_name='Dificultad')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Termino'
        verbose_name_plural = 'Terminos'
        ordering = ['-creado_en']

    def __str__(self):
        return self.palabra


class Variante(models.Model):
    termino_base = models.ForeignKey(Termino, on_delete=models.CASCADE, related_name='variantes')
    palabra_variante = models.CharField(max_length=100, verbose_name='Variante')
    pais = models.CharField(max_length=50, verbose_name='Pais/Region')
    explicacion = models.TextField(blank=True, verbose_name='Contexto de uso')
    frecuencia_uso = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Variante Lexica'
        verbose_name_plural = 'Variantes Lexicas'

    def __str__(self):
        return self.palabra_variante + ' (' + self.pais + ')'


class UserProfile(models.Model):
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')
    bio = models.TextField(blank=True, max_length=500)
    pais = models.CharField(max_length=50, blank=True)
    avatar = models.URLField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return 'Perfil de ' + self.user.username


@receiver(post_save, sender=User)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)



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
