from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect to accounts
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    # Accounts View's
    path('accounts/', include('accounts.urls')),
    # Dashboard Admin
    path('superadmin/', include('dashboarda.urls')),
    # Dashboard Junta de Vecinos
    path('juntavecinos/', include('dashboardjv.urls')),
    # Dashboard Vecino
    path('vecino/', include('dashboardv.urls')),
    
]
