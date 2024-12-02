from django.urls import path
from .views import DashboardJuntaVecino, ListaVecinosView, CrearVecinoTitularView, EditarVecinoTitular, CrearVecinoMiembroView, EditarVecinoMiembroView, ListaMiembrosFamilia, ListaNoticias, CrearNoticia, EditarNoticia, ListaCertificados, CrearCertificado, EditarCertificado, vecinos_chart_data, reset_data, filter_data, ListaActividades, CrearActividad
from .utils import BuscarPerfil

app_name = "dashboardjv"

urlpatterns = [
    # APIS
    path('buscar-perfil/', BuscarPerfil.as_view(), name='buscar_perfil'),
    
    # URLS
    path('dashboard/', DashboardJuntaVecino.as_view(), name='juntavecinos'),
    
    path('dashboard/filter_data/', filter_data, name='filter_data'),
    path('dashboard/reset_data/', reset_data, name='reset_data'),
    path('dashboard/vecinos_chart_data/', vecinos_chart_data, name='vecinos_chart_data'),
    
    # Vecinos
    path('vecinos/', ListaVecinosView.as_view(), name='listavecinos'),
    path('vecinos/crear/', CrearVecinoTitularView.as_view(), name='crearvecino'),
    path('vecinos/editar/<int:rut>/', EditarVecinoTitular.as_view(), name='editarvecino'),
    
    # Vecinos - Noticias
    path('noticias/', ListaNoticias.as_view(), name='listanoticias'),
    path('noticias/crear/', CrearNoticia.as_view(), name='crearnoticia'),
    path('noticias/editar/<int:id_noticia>/', EditarNoticia.as_view(), name='editarnoticia'),
    
    # Vecinos - Certificados de residencia
    path('certificados/', ListaCertificados.as_view(), name='listacertificados'),
    path('certificados/crear/', CrearCertificado.as_view(), name='crearcertificado'),
    path('certificados/editar/<int:id_certificado>/', EditarCertificado.as_view(), name='editarcertificado'),
    
    
    # Vecinos - Actividades
    path('actividades/', ListaActividades.as_view(), name='listaactividades'),
    path('actividades/crear/', CrearActividad.as_view(), name='crearactividad'),
    
    # Vecinos - Familia
    path('vecinos/familia/<int:rut>/', ListaMiembrosFamilia.as_view(), name='lista_familia'),
    path('vecinos/familia/<int:rut>/crear/', CrearVecinoMiembroView.as_view(), name='crear_miembro_familia'),
    path('vecinos/familia/<int:titular_rut>/editar/<int:rut>/', EditarVecinoMiembroView.as_view(), name='editar_miembro_familia'),
    
]