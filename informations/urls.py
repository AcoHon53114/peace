from django.urls import path
from . import views

urlpatterns = [
    path('informations', views.information, name='information'),
    path('guideline', views.guideline, name='guideline'),
]

