from django.urls import path
from . import views

urlpatterns = [
    path('', views.information, name='information'),  # 新增這一行
    path('informations', views.information, name='information'),
    path('guideline', views.guideline, name='guideline'),
]