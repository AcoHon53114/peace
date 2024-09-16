from django.urls import path
from . import views

urlpatterns = [
    path('environments', views.environment, name='environment'),
]