from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from .models import Perfiles


# Esto es una vista personalizada de Incio de Sesión
class CustomLoginView(LoginView):
    def get_succes_url(self):
        user = self.request.user
        if user.id_rol.descripcion == "Administrador":
            pass
        elif user.id_rol.descripcion == "Junta de Vecino":
            pass
        elif user.id_rol.descripcion == "Vecino":
            pass
        else:
            pass