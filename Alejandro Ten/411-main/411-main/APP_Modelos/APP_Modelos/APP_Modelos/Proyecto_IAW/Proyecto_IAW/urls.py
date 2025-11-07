# Proyecto_IAW/urls.py
from django.contrib import admin
from django.urls import path
from Impuesto_411 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.formulario_411, name='formulario_411'),           # GET → formulario
    path('api/impuesto411/', views.impuesto_411_api, name='api_411') # POST → API
]
