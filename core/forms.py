from django import forms
from .models import Termino


class TerminoForm(forms.ModelForm):
    """
    Formulario para crear/editar términos con campos lexicográficos completos.
    Los campos JSONField se editan como texto (una entrada por línea).
    """

    class Meta:
        model = Termino
        fields = [
            'palabra', 'categoria_gramatical', 'definicion',
            'acepciones', 'etimologia', 'ejemplo',
            'sinonimos', 'antonimos', 'familia_lexica', 'locuciones',
            'nivel', 'frecuencia', 'marcas',
            'categoria_semantica', 'dificultad',
        ]
        widgets = {
            'palabra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: casa, amor, aprender'
            }),
            'categoria_gramatical': forms.Select(attrs={'class': 'form-select'}),
            'definicion': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Definición principal'
            }),
            'acepciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Una acepción por línea'
            }),
            'etimologia': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Ej: Del latín "casa"'
            }),
            'ejemplo': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Ej: Mi casa está cerca'
            }),
            'sinonimos': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Uno por línea'
            }),
            'antonimos': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Uno por línea'
            }),
            'familia_lexica': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Uno por línea'
            }),
            'locuciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Una por línea'
            }),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'frecuencia': forms.Select(attrs={'class': 'form-select'}),
            'marcas': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Una por línea'
            }),
            'categoria_semantica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: emoción, naturaleza'
            }),
            'dificultad': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'palabra': 'Palabra (lema)',
            'categoria_gramatical': 'Categoría gramatical',
            'definicion': 'Definición principal',
            'acepciones': 'Acepciones adicionales',
            'etimologia': 'Etimología',
            'ejemplo': 'Ejemplo de uso',
            'sinonimos': 'Sinónimos',
            'antonimos': 'Antónimos',
            'familia_lexica': 'Familia léxica',
            'locuciones': 'Locuciones',
            'nivel': 'Nivel de uso',
            'frecuencia': 'Frecuencia de uso',
            'marcas': 'Marcas de uso',
            'categoria_semantica': 'Categoría semántica',
            'dificultad': 'Dificultad',
        }

    # Convertir campos lista (JSONField) desde texto multilínea
    def _clean_json_list(self, field_name):
        value = self.cleaned_data.get(field_name)
        if isinstance(value, str):
            return [line.strip() for line in value.split('\n') if line.strip()]
        if isinstance(value, list):
            return value
        return []

    def clean_acepciones(self):
        return self._clean_json_list('acepciones')

    def clean_sinonimos(self):
        return self._clean_json_list('sinonimos')

    def clean_antonimos(self):
        return self._clean_json_list('antonimos')

    def clean_familia_lexica(self):
        return self._clean_json_list('familia_lexica')

    def clean_locuciones(self):
        return self._clean_json_list('locuciones')

    def clean_marcas(self):
        return self._clean_json_list('marcas')



# ═══════════════════════════════════════════════════════
# FORMULARIOS DE USUARIO
# ═══════════════════════════════════════════════════════

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'tu@email.com'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nombre de usuario'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Contrasena'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Repite la contrasena'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)
        return user


class PerfilForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['rol', 'bio', 'pais', 'avatar', 'fecha_nacimiento']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Cuentanos sobre ti...'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ej: Colombia'
            }),
            'avatar': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://...'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
        }
        labels = {
            'rol': 'Rol',
            'bio': 'Biografia',
            'pais': 'Pais',
            'avatar': 'URL del avatar',
            'fecha_nacimiento': 'Fecha de nacimiento',
        }


# ═══════════════════════════════════════════════════════
# FORMULARIO DE TRADUCCIONES
# ═══════════════════════════════════════════════════════

from .models import TraduccionTermino


class TraduccionForm(forms.ModelForm):
    """Formulario para aportar una traducción de un término."""

    class Meta:
        model = TraduccionTermino
        fields = [
            'idioma', 'traduccion', 'definicion_nativa',
            'ejemplo_nativo', 'nivel_correspondencia', 'notas',
        ]
        widgets = {
            'idioma': forms.Select(attrs={'class': 'form-select'}),
            'traduccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: house'
            }),
            'definicion_nativa': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Definición en el idioma nativo (opcional)'
            }),
            'ejemplo_nativo': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Ejemplo de uso en el idioma nativo (opcional)'
            }),
            'nivel_correspondencia': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Notas para el revisor (opcional)'
            }),
        }
        labels = {
            'idioma': 'Idioma',
            'traduccion': 'Traducción',
            'definicion_nativa': 'Definición en el idioma nativo',
            'ejemplo_nativo': 'Ejemplo en el idioma nativo',
            'nivel_correspondencia': 'Nivel de correspondencia',
            'notas': 'Notas',
        }