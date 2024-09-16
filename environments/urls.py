from django.urls import path
from . import views

urlpatterns = [
    path('', views.environment, name='environment'),  # 新增這一行
    path('environments', views.environment, name='environment'),
]