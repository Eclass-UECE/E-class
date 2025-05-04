from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagInicial, name='pagInicial'),
]