from django.urls import path
from .views import DashboardAdminView, CrearJuntaVecinosView, EditarJuntaVecinosView, JuntaVecinosView, JuntaVecinosRegiones,PerfilesVecinosView, CrearPerfilVecinoView, EditarPerfilVecinoView, PerfilesJuntaVecino,load_comunas, get_perfiles_by_comuna, filter_data, reset_data, juntas_chart_data, juntas_por_region_chart_data, obtener_juntas_vecinos

app_name = "dashboarda"


urlpatterns = [
    path('load-comunas/', load_comunas, name='load_comunas'),
    path('get_perfiles_by_comuna/<int:comuna_id>/', get_perfiles_by_comuna, name='get_perfiles_by_comuna'),
    
    # Dashboard
    path('dashboard/', DashboardAdminView.as_view(), name='superadmin'),
    path("dashboard/filter_data/", filter_data, name="filter_data"),
    path("dashboard/reset_data/", reset_data, name="reset_data"),
    path('dashboard/juntas_chart_data/', juntas_chart_data, name='juntas_chart_data'),
    path('dashboard/juntas_por_region_chart_data/', juntas_por_region_chart_data, name='juntas_por_region_chart_data'),
    
    # Api del administrador
    path('api/juntas/', obtener_juntas_vecinos, name='obtener_juntas_vecinos'),
    
    
    # C R U JUNTA DE VECINOS
    path('juntavecinos/crear/', CrearJuntaVecinosView.as_view(), name='crear_juntavecinos'),
    path('juntavecinos/', JuntaVecinosView.as_view(), name='juntavecinos'),
    path('juntavecinos/editar/<int:id_juntavecino>/', EditarJuntaVecinosView.as_view(), name='editar_juntavecinos'),
    
    path('juntavecinos/perfiles/<int:id_juntavecino>/', PerfilesJuntaVecino.as_view(), name='perfiles_junta'),
    path('juntavecinos/mapa/', JuntaVecinosRegiones.as_view(), name='mapa'),
    
    # C R U PERFILES ASOCIADOS
    path('perfiles/crear/', CrearPerfilVecinoView.as_view(), name='crear_perfil'),
    path('perfiles/', PerfilesVecinosView.as_view(), name='perfiles'),
    path('perfiles/editar/<str:rut>/', EditarPerfilVecinoView.as_view(), name='editar_perfil_junta'),
    
]
