from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts View's
    path('accounts/', include('accounts.urls')),
    # Dashboard Admin
    path('superadmin/', include('dashboarda.urls')),
    # Dashboard Junta de Vecinos
    path('juntavecinos/', include('dashboardjv.urls')),
    # Dashboard Vecino
    path('vecino/', include('dashboardv.urls')),
    
]
