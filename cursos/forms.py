from django import forms
from .models import Curso, Leccion, Ejercicio


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descripcion', 'icono', 'categoria_semantica', 'nivel']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Vocabulario de Animales'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripcion del curso'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'placeholder': 'Ej: A'
            }),
            'categoria_semantica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: naturaleza, sociedad'
            }),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
        }


class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = ['titulo', 'subclase', 'orden', 'teoria', 'xp_reward']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Introduccion a los animales'
            }),
            'subclase': forms.Select(attrs={'class': 'form-select'}),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'teoria': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Contenido teorico de la leccion'
            }),
            'xp_reward': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = [
            'orden', 'pregunta',
            'opcion_a', 'opcion_b', 'opcion_c', 'opcion_d',
            'respuesta_correcta', 'explicacion', 'xp_reward'
        ]
        widgets = {
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'pregunta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cual es la palabra...?'
            }),
            'opcion_a': forms.TextInput(attrs={'class': 'form-control'}),
            'opcion_b': forms.TextInput(attrs={'class': 'form-control'}),
            'opcion_c': forms.TextInput(attrs={'class': 'form-control'}),
            'opcion_d': forms.TextInput(attrs={'class': 'form-control'}),
            'respuesta_correcta': forms.Select(
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                attrs={'class': 'form-select'}
            ),
            'explicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Explicacion de la respuesta correcta'
            }),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }