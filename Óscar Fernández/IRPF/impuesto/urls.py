from django.urls import path
from . import views
urlpatterns = [
    path('', views.declarar_irpf, name='declarar_irpf'),
    path('resultado/<int:pk>/', views.resultado_irpf, name='resultado_irpf'),
]