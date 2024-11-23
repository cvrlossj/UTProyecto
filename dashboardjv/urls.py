from django.urls import path
from .views import DashboardJuntaVecino

app_name = "dashboardjv"

urlpatterns = [
    # URLS
    path('dashboard/', DashboardJuntaVecino.as_view(), name='juntavecinos'),
]