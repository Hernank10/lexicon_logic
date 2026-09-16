from django.db import models
from django.contrib.auth.models import User
from core.models import Termino
import uuid


class Curso(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Basico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=10, default='')
    categoria_semantica = models.CharField(max_length=50, db_index=True)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    xp_total = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria_semantica', 'nivel']

    def __str__(self):
        return self.titulo


class Leccion(models.Model):
    SUBCLASE_CHOICES = [
        ('intro', 'Introduccion'),
        ('practica', 'Practica'),
        ('evaluacion', 'Evaluacion'),
    ]
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    subclase = models.CharField(max_length=20, choices=SUBCLASE_CHOICES, default='intro')
    orden = models.IntegerField(default=1)
    teoria = models.TextField(blank=True)
    xp_reward = models.IntegerField(default=20)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['curso', 'orden']

    def __str__(self):
        return self.titulo


class Ejercicio(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='ejercicios')
    termino = models.ForeignKey(Termino, on_delete=models.SET_NULL, null=True, blank=True)
    orden = models.IntegerField(default=1)
    pregunta = models.TextField()
    opcion_a = models.CharField(max_length=200)
    opcion_b = models.CharField(max_length=200)
    opcion_c = models.CharField(max_length=200, blank=True)
    opcion_d = models.CharField(max_length=200, blank=True)
    respuesta_correcta = models.CharField(max_length=1, default='A')
    explicacion = models.TextField(blank=True)
    xp_reward = models.IntegerField(default=10)

    class Meta:
        ordering = ['leccion', 'orden']

    def __str__(self):
        return self.pregunta[:50]


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    xp_acumulado = models.IntegerField(default=0)
    progreso = models.IntegerField(default=0)
    completado = models.BooleanField(default=False)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('estudiante', 'curso')
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return self.estudiante.username + ' -> ' + self.curso.titulo

    @property
    def nivel(self):
        return 1 + (self.xp_acumulado // 100)

    @property
    def xp_siguiente_nivel(self):
        return 100 - (self.xp_acumulado % 100)

    @property
    def lecciones_totales(self):
        return self.curso.lecciones.count()

    @property
    def lecciones_completadas(self):
        return self.progresos.filter(completada=True).count()

    def actualizar_progreso(self):
        total = self.lecciones_totales
        if total == 0:
            self.progreso = 0
        else:
            completadas = self.lecciones_completadas
            self.progreso = int((completadas / total) * 100)
        self.completado = self.progreso >= 100
        self.save()


class ProgresoLeccion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='progresos')
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='progresos')
    completada = models.BooleanField(default=False)
    xp_ganado = models.IntegerField(default=0)
    aciertos = models.IntegerField(default=0)
    errores = models.IntegerField(default=0)
    fecha_completado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('inscripcion', 'leccion')
        ordering = ['leccion__orden']

    def __str__(self):
        return self.inscripcion.estudiante.username + ' - ' + self.leccion.titulo


class Certificado(models.Model):
    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='certificado')
    codigo = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    xp_final = models.IntegerField(default=0)
    puntaje = models.IntegerField(default=0)

    class Meta:
        ordering = ['-fecha_emision']

    def __str__(self):
        return 'Cert ' + self.codigo + ' - ' + self.inscripcion.estudiante.username

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = 'CERT-' + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)