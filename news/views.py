from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'news/news.html',)

def new(request):
    return render(request, 'news/new.html',)
