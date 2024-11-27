from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Vistas
from django.views.generic import TemplateView, View
# Utilidades
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
# Modelos Propios
from accounts.models import Perfiles, Sexo, Parentesco
from dashboardjv.models import JuntaVecinos, CertificadosResi


# Editar Perfil
@method_decorator(login_required, name='dispatch')
class EditarPerfil(View):
     def get(self, request, *args, **kwargs):
          user = self.request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          vecino = get_object_or_404(Perfiles, rut=request.user.rut)
          sexos = Sexo.objects.all()
          parentescos = Parentesco.objects.all()
          
          context = {
               'user': user,
               'junta': junta,
               'sexos': sexos,
               'parentescos': parentescos,
          }
          return render(request, 'dashboardv/editarperfil.html', context)
          

     def post(self, request, *args, **kwargs):
          user = request.user
          vecino = get_object_or_404(Perfiles, rut=user.rut)
          # Obtenemos los datos del formulario
          numero_contacto = request.POST.get('numero_contacto')
          email = request.POST.get('email')
          contrasena = request.POST.get('contrasena')

          
          if not all([numero_contacto, email]):
               messages.error(request, 'Todos los campos son obligatorios.')
               return redirect('dashboarda:editarperfilvecino')
          
          try:
               vecino.numero_contacto = numero_contacto
               vecino.correo_electronico = email
               if contrasena:
                    vecino.set_password(contrasena)
               vecino.save()
               messages.success(request, 'Perfil actualizado correctamente.')
               return redirect('dashboardv:editarperfilvecino')
          
          except Exception as e:
               messages.error(request, f'Ocurrió un error al actualizar el perfil: {str(e)}')
               return redirect('dashboardv:editarperfilvecino')



# ! [--- Certificado de Residencia ---]
@method_decorator(login_required, name='dispatch')
class ListaCertificados(View):
    def get(self, request, *args, **kwargs):
          user = request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          certificados = CertificadosResi.objects.filter(id_juntavecinos=junta, rut_postulante=user.rut)
          
          context = {
               'user': user,
               'junta': junta,
               'certificados': certificados,
          }
          return render(request, 'dashboardv/certificados/listacertificados.html', context)






# ! Dashboard
@method_decorator(login_required, name='dispatch')
class DashboardVecino(TemplateView):
     template_name = 'dashboardv/dashboardv.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          user = self.request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          
          context.update({
               'user': user,
               'junta': junta,
          })
          return context
