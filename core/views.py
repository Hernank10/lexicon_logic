from django.shortcuts import render, redirect
from .models import Termino
from .forms import TerminoForm

def home(request):
    # Lógica para la creación (POST)
    if request.method == 'POST':
        form = TerminoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    # Lógica para la búsqueda (GET)
    query = request.GET.get('q')
    form = TerminoForm() # Formulario vacío para el modal

    if query:
        terminos = Termino.objects.filter(palabra__icontains=query)
    else:
        terminos = Termino.objects.all().order_by('-creado_en')[:5]

    return render(request, 'index.html', {
        'terminos': terminos, 
        'query': query,
        'form': form
    })
