from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import New
from django.shortcuts import render, get_object_or_404
from urllib.parse import urlparse, parse_qs

# Create your views here.

def index(request):
    news = New.objects.order_by('-list_date').filter(is_published=True)
    #get all data from listing database
    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    print(page)
    paged_news = paginator.get_page(page)
    
    context = {'news' : paged_news}
    return render(request, 'news/news.html', context)

def new(request, new_id):
    new = get_object_or_404(New, pk=new_id)
    context = {'new': new}
    print(f"YouTube URL: {new.youtube_link}")
    return render(request,'news/new.html', context)

def search(request):
    queryset_list = New.objects.order_by('-list_date')
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            queryset_list = queryset_list.filter(
                title__icontains=title
                )
        context = {
                'news':queryset_list,
                'values':request.GET,
                }
    return render(request,'news/news.html', context)