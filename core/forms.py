from django import forms
from .models import Termino

class TerminoForm(forms.ModelForm):
    class Meta:
        model = Termino
        fields = ['palabra', 'definicion', 'categoria_gramatical']
        
        # Agregamos estilos de Bootstrap para que se vea profesional
        widgets = {
            'palabra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Trabajo'}),
            'definicion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción...'}),
            'categoria_gramatical': forms.Select(attrs={'class': 'form-select'}),
        }
