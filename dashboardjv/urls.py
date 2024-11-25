from django.urls import path
from .views import DashboardJuntaVecino, ListaVecinosView, CrearVecinoTitularView, EditarVecinoTitular, CrearVecinoMiembroView, EditarVecinoMiembroView, ListaMiembrosFamilia, ListaNoticias, CrearNoticia, EditarNoticia 

app_name = "dashboardjv"

urlpatterns = [
    # URLS
    path('dashboard/', DashboardJuntaVecino.as_view(), name='juntavecinos'),
    
    # Vecinos
    path('vecinos/', ListaVecinosView.as_view(), name='listavecinos'),
    path('vecinos/crear/', CrearVecinoTitularView.as_view(), name='crearvecino'),
    path('vecinos/editar/<int:rut>/', EditarVecinoTitular.as_view(), name='editarvecino'),
    
    # Vecinos - Noticias
    path('noticias/', ListaNoticias.as_view(), name='listanoticias'),
    path('noticias/crear/', CrearNoticia.as_view(), name='crearnoticia'),
    path('noticias/editar/<int:id_noticia>/', EditarNoticia.as_view(), name='editarnoticia'),
    
    # Vecinos - Certificados de residencia
    
    # Vecinos - Familia
    path('vecinos/familia/<int:rut>/', ListaMiembrosFamilia.as_view(), name='lista_familia'),
    path('vecinos/familia/<int:rut>/crear/', CrearVecinoMiembroView.as_view(), name='crear_miembro_familia'),
    path('vecinos/familia/<int:titular_rut>/editar/<int:rut>/', EditarVecinoMiembroView.as_view(), name='editar_miembro_familia'),
    
]