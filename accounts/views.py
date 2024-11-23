from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .models import Perfiles
from django.contrib.auth import logout
from django.views.generic import View

# Esto es una vista personalizada de Incio de Sesión
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        
        if user.id_estadoperfil and user.id_estadoperfil.descripcion != "habilitado":
            return reverse("accounts:login")
        
        if user.id_rol.descripcion == "Administrador":
            return reverse('dashboarda:superadmin') 
        elif user.id_rol.descripcion == "Junta Vecinos":
            return reverse('dashboardjv:juntavecinos')
        elif user.id_rol.descripcion == "Vecino":
            pass
        
        return reverse('accounts:login')
    

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")