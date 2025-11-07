from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_576, name='formulario_576'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]
