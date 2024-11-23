from django.shortcuts import render
# Vistas Genericas
from django.views.generic import TemplateView, View
# Utilidades
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class DashboardJuntaVecino(TemplateView):
    template_name = "dashboardjv/dashboardjuntavecino.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard Junta de Vecinos'
        user = self.request.user
        
        context.update({
            'user': user,
        })
        
        return context