from django.shortcuts import render
from environments.models import Voice  # Corrected the import statement

# Create your views here.

def environment(request):
    voices = Voice.objects.filter(is_published=True)  # Corrected the variable name
    context = {'voices': voices}  # Corrected the context variable name
    return render(request, 'environments/environment.html', context)
