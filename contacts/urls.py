from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),  # 新增這一行
    path('contacts', views.contact, name='contact'),
]