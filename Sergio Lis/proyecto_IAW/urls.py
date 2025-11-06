from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app_IAW.views import Modelo146ViewSet, EntidadPagadoraViewSet, home, formulario_146

router = routers.DefaultRouter()
router.register(r'modelo146', Modelo146ViewSet)
router.register(r'entidades', EntidadPagadoraViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),       # API REST
    path('', home, name='home'),              # Página home
    path('formulario146/', formulario_146, name='formulario146'),  # Formulario HTML
]
