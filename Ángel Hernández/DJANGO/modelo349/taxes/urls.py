from django.urls import path
from .views import HomeView, DeclaracionListCreateAPI, SujetoListCreateAPI, export_declaracion_csv

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/declaraciones/', DeclaracionListCreateAPI.as_view(), name='api-declaraciones'),
    path('api/sujetos/', SujetoListCreateAPI.as_view(), name='api-sujetos'),
    path('export/<int:pk>/', export_declaracion_csv, name='export-csv'),
]
