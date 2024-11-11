from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Accounts View's
    path('accounts/', include('accounts.urls')),
]
