from .models import Idioma


def idiomas_disponibles(request):
    """Inyecta la lista de idiomas y el idioma actual en todos los templates."""
    return {
        'idiomas_disponibles': Idioma.objects.filter(activo=True).order_by('-hablantes_millones'),
        'idioma_actual': request.session.get('idioma', 'es'),
    }