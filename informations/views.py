from django.shortcuts import render

def information(request):
    return render(request, 'informations/information.html',)

def guideline(request):
    return render(request, 'informations/guideline.html',)
