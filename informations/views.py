from django.shortcuts import render

# Create your views here.

def information(request):
    return render(request, 'informations/information.html',)

def guideline(request):
    return render(request, 'informations/guideline.html',)
