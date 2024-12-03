from django.urls import path
from .views import DashboardVecino, EditarPerfil, ListaFamilia, ListaCertificados, SolicitarCertificadoResidencia, ListaActividades, InscribirseActividad, CancelarInscripcion
from .utils import BuscarMiembroPerfil, ObtenerMiembrosFamilia


app_name = "dashboardv"

urlpatterns = [
    
    # APIS 
    path('buscar-miembros/', BuscarMiembroPerfil.as_view(), name='buscar_miembros'),
    path('buscar-miembros-all/', ObtenerMiembrosFamilia.as_view(), name='buscar_miembros_all'),
    
    path('dashboard/', DashboardVecino.as_view(), name='dashboardvecino'),
    
    # Editar Perfil
    path('editarperfil/', EditarPerfil.as_view(), name='editarperfilvecino'),
    
    # Miembros de la familia
    path('miembros/', ListaFamilia.as_view(), name='listafamilia'),
    
    # Certificados de Residencia
    path('certificados/', ListaCertificados.as_view(), name='listacertificados'),
    path('certificados/crear/', SolicitarCertificadoResidencia.as_view(), name='crearcertificado'),
    
    # Actividades
    path('actividades/', ListaActividades.as_view(), name='listaactividades'),
    path('actividades/inscribirse/<int:id_actividad>/', InscribirseActividad.as_view(), name='inscribirseactividad'),
    path('actividad/<int:id_actividad>/cancelar_inscripcion/<int:id_inscripcion>/', CancelarInscripcion.as_view(), name='cancelar_inscripcion'),
    
]
