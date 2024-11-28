from django.urls import path
from .views import DashboardVecino, EditarPerfil, ListaFamilia, ListaCertificados, SolicitarCertificadoResidencia
from .utils import BuscarMiembroPerfil


app_name = "dashboardv"

urlpatterns = [
    
    # APIS 
    path('buscar-miembros/', BuscarMiembroPerfil.as_view(), name='buscar_miembros'),
    
    path('dashboard/', DashboardVecino.as_view(), name='dashboardvecino'),
    
    # Editar Perfil
    path('editarperfil/', EditarPerfil.as_view(), name='editarperfilvecino'),
    
    # Miembros de la familia
    path('miembros/', ListaFamilia.as_view(), name='listafamilia'),
    
    # Certificados de Residencia
    path('certificados/', ListaCertificados.as_view(), name='listacertificados'),
    path('certificados/crear/', SolicitarCertificadoResidencia.as_view(), name='crearcertificado'),
    
]
