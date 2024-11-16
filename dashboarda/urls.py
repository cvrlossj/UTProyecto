from django.urls import path
from .views import DashboardAdminView, JuntaVecinosView, load_comunas, get_perfiles_by_comuna

app_name = "dashboarda"


urlpatterns = [
    path('dashboard/', DashboardAdminView.as_view(), name='superadmin'),
    path('juntavecinos/', JuntaVecinosView.as_view(), name='juntavecinos'),
    path('load-comunas/', load_comunas, name='load_comunas'),
    path('get_perfiles_by_comuna/<int:comuna_id>/', get_perfiles_by_comuna, name='get_perfiles_by_comuna'),
]
