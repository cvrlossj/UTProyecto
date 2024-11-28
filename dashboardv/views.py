from django.http import JsonResponse
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
from dashboardjv.models import JuntaVecinos, CertificadosResi, EstadoCertificado


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



@method_decorator(login_required, name='dispatch')
class ListaCertificados(View):
    def get(self, request, *args, **kwargs):
          user = request.user

          # Obtener la junta de vecinos del usuario
          junta = get_object_or_404(JuntaVecinos, perfiles=user)

          # Obtener los IDs de los miembros de la familia del titular (incluyéndose a sí mismo)
          if user.familia:  # Si pertenece a una familia
               miembros_ids = user.familia.miembros.values_list('rut', flat=True)
          else:
               # Si no pertenece a una familia, solo se filtra por su propio rut
               miembros_ids = [user.rut]

          # Filtrar certificados de residencia de los miembros de la familia
          certificados = CertificadosResi.objects.filter(
               id_juntavecinos=junta,
               rut_postulante__in=miembros_ids  # Filtrar por los RUTs obtenidos
          )

          context = {
               'user': user,
               'junta': junta,
               'certificados': certificados,
          }
          return render(request, 'dashboardv/certificados/listacertificados.html', context)


@method_decorator(login_required, name='dispatch')
class SolicitarCertificadoResidencia(View):
     def get(self, request, *args, **kwargs):
          """
          Renderiza la página para solicitar un certificado.
          """
          user = request.user

          # Obtener la junta de vecinos del usuario
          junta = get_object_or_404(JuntaVecinos, perfiles=user)

          context = {
               'user': user,
               'junta': junta,
          }
          return render(request, 'dashboardv/certificados/crearcertificado.html', context)

     def post(self, request, *args, **kwargs):
          """
          Maneja la creación de un nuevo certificado.
          """
          user = request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)

          # Recuperar datos del formulario
          rut = request.POST.get('rut', '').strip()
          nombre = request.POST.get('nombre', '').strip()
          apellido = request.POST.get('apellido', '').strip()
          email = request.POST.get('email', '').strip()
          direccion = request.POST.get('direccion', '').strip()

          # Validar datos básicos
          if not (rut and nombre and email and direccion):
               messages.error(request, 'Todos los campos son obligatorios.')
               return redirect('dashboardv:crearcertificado')

          try:
               # Obtener el estado inicial del certificado
               estado_certificado = get_object_or_404(EstadoCertificado, id_estadocertificado=1)

               # Crear el certificado
               CertificadosResi.objects.create(
                    id_juntavecinos=junta,
                    nombre_postulante=nombre,
                    direccion_postulante=direccion,
                    rut_postulante=get_object_or_404(Perfiles, rut=rut),
                    id_estadocertificado=estado_certificado
               )

               # Mensaje de éxito
               messages.success(request, 'Certificado creado con éxito.')
               return redirect('dashboardv:listacertificados')

          except Exception as e:
               # Mensaje de error si ocurre algún problema
               messages.error(request, f"Hubo un error al procesar el certificado: {str(e)}")
               return redirect('dashboardv:crearcertificado')




# ! Dashboard
@method_decorator(login_required, name='dispatch')
class DashboardVecino(TemplateView):
     template_name = 'dashboardv/dashboardv.html'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          user = self.request.user
          
          titular = get_object_or_404(Perfiles, rut=user.rut, id_parentesco__descripcion="Titular")
          
          familia = titular.familia
          
          if not familia:
               messages.error(self.request, 'No perteneces a ninguna familia.')
               return redirect('dashboardv:dashboardvecino')
          
          
          # Obtener todos los vecinos asociados a esta familia
          miembros_total = familia.miembros.all().count()
          miembros_contar_habilitar = familia.miembros.filter(id_estadoperfil=1).count()
          miembros_contar_inhabilitar = familia.miembros.filter(id_estadoperfil=2).count()
          
          
          
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          
          context.update({
               'user': user,
               'junta': junta,
               'miembros_total': miembros_total,
               'miembros_contar_habilitar': miembros_contar_habilitar,
               'miembros_contar_inhabilitar': miembros_contar_inhabilitar,
          })
          return context
