from django.urls import path
from .views import DashboardVecino, EditarPerfil, ListaCertificados

app_name = "dashboardv"

urlpatterns = [
    path('dashboard/', DashboardVecino.as_view(), name='dashboardvecino'),
    
    # Editar Perfil
    path('editarperfil/', EditarPerfil.as_view(), name='editarperfilvecino'),
    
    # Certificados de Residencia
    path('certificados/', ListaCertificados.as_view(), name='listacertificados'),
    path('certificados/crear/', ListaCertificados.as_view(), name='crearcertificado'),
    
]
