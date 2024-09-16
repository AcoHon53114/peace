from django.shortcuts import render

# Create your views here.

def environment(request):
    return render(request, 'environments/environment.html',)
