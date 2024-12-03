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
from django.db.models import Prefetch
from accounts.models import Perfiles, Sexo, Parentesco
from dashboardjv.models import JuntaVecinos, CertificadosResi, EstadoCertificado, Actividad, InscripcionActividad
from dashboarda.utils import role_required


@method_decorator([login_required, role_required(3)], name='dispatch')
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



@method_decorator([login_required, role_required(3)], name='dispatch')
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


@method_decorator([login_required, role_required(3)], name='dispatch')
class SolicitarCertificadoResidencia(View):
     def get(self, request, *args, **kwargs):
          """
          Renderiza la página para solicitar un certificado.
          """
          user = request.user

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
               estado_certificado = get_object_or_404(EstadoCertificado, id_estadocertificado=1)

               CertificadosResi.objects.create(
                    id_juntavecinos=junta,
                    nombre_postulante=nombre,
                    direccion_postulante=direccion,
                    rut_postulante=get_object_or_404(Perfiles, rut=rut),
                    id_estadocertificado=estado_certificado
               )

               messages.success(request, 'Certificado solicitado con éxito.')
               return redirect('dashboardv:listacertificados')

          except Exception as e:
               messages.error(request, f"Hubo un error al procesar el certificado: {str(e)}")
               return redirect('dashboardv:crearcertificado')


@method_decorator([login_required, role_required(3)], name='dispatch')
class ListaFamilia(View):
    def get(self, request, *args, **kwargs):
          user = request.user

          # Obtener la junta de vecinos del usuario
          junta = get_object_or_404(JuntaVecinos, perfiles=user)

          # Obtener el titular y miembros de la familia
          titular = user  # Asumimos que `user` es el titular de la familia
          miembros = Perfiles.objects.filter(familia=user.familia) if user.familia else []

          # Filtrar certificados de residencia
          certificados = CertificadosResi.objects.filter(
               id_juntavecinos=junta,
               rut_postulante__in=miembros.values_list('rut', flat=True) if miembros else [user.rut]
          )

          context = {
               'user': user,
               'junta': junta,
               'certificados': certificados,
               'miembros': miembros,  # Lista de miembros de la familia
               'titular': titular,    # Información del titular
          }
          return render(request, 'dashboardv/listamiembrosfamilia.html', context)


@method_decorator([login_required, role_required(3)], name='dispatch')
class ListaActividades(View):
     def get(self, request, *args, **kwargs):
          user = request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          
          actividades = Actividad.objects.filter(
               id_juntavecinos=junta
          )
          
          # Cupos tomados para está actividad
          for actividad in actividades:
               actividad.cupos_tomados = InscripcionActividad.objects.filter(id_actividad=actividad).count()
          
          context = {
               'user': user,
               'junta': junta,
               'actividades': actividades,
               'cupos_tomados': actividad.cupos_tomados,
          }
          return render(request, 'dashboardv/actividades/listaactividades.html', context)

@method_decorator([login_required, role_required(3)], name='dispatch')
class InscribirseActividad(View):
     def get(self, request, id_actividad, *args, **kwargs):
          user = request.user
          junta = get_object_or_404(JuntaVecinos, perfiles=user)
          
          actividad = get_object_or_404(Actividad, id_actividad=id_actividad)
          inscripciones = InscripcionActividad.objects.filter(id_actividad=actividad)
          familia_usuario = user.familia
          
          miembros = Perfiles.objects.filter(
               inscripcionactividad__id_actividad=actividad,
               inscripcionactividad__id_perfil__in=junta.perfiles.all(),
               familia=familia_usuario
          ).prefetch_related(
               Prefetch('inscripcionactividad_set', queryset=inscripciones, to_attr='inscripciones')
          ).distinct()
          
          context = {
               'user': user,
               'junta': junta,
               'actividad': actividad,
               'miembros': miembros,
          }
          return render(request, 'dashboardv/actividades/inscribirseactividad.html', context)
          
     def post(self, request, id_actividad, *args, **kwargs):
          user = request.user
          actividad = get_object_or_404(Actividad, id_actividad=id_actividad)

          # Obtener el miembro seleccionado desde el formulario
          perfil_rut = request.POST.get('rut')
          perfil = get_object_or_404(Perfiles, rut=perfil_rut)
          
          # Verificar si ya está inscrito
          if InscripcionActividad.objects.filter(id_perfil=perfil, id_actividad=actividad).exists():
               messages.error(request, 'El miembro ya está inscrito en esta actividad.')
               return redirect('dashboardv:inscribirseactividad', id_actividad=id_actividad)
          
          # Verificar si hay cupos disponibles
          if actividad.cupos <= InscripcionActividad.objects.filter(id_actividad=actividad).count():
               messages.error(request, 'No hay cupos disponibles para esta actividad.')
               return redirect('dashboardv:inscribirseactividad', id_actividad=id_actividad)
          
          # Crear la inscripción
          try:
               inscripcion = InscripcionActividad(id_perfil=perfil, id_actividad=actividad)
               inscripcion.save()
               messages.success(request, f'{perfil.nombre} {perfil.apellido} ha sido inscrito con éxito en la actividad.')
               return redirect('dashboardv:inscribirseactividad', id_actividad=id_actividad)
          except Exception as e:
               messages.error(request, f'Error al inscribir: {str(e)}')
               return redirect('dashboardv:inscribirseactividad', id_actividad=id_actividad)

@method_decorator([login_required, role_required(3)], name='dispatch')
class CancelarInscripcion(View):
     def get(self, request, id_actividad, id_inscripcion, *args, **kwargs):
          inscripcion = get_object_or_404(InscripcionActividad, id_inscripcion=id_inscripcion)
          
          try:
               inscripcion.delete()
               messages.success(request, 'Inscripción cancelada con éxito.')
          except Exception as e:
               messages.error(request, f'Error al cancelar inscripción: {str(e)}')
          return redirect('dashboardv:inscribirseactividad', id_actividad=id_actividad)
          


# ! Dashboard
@method_decorator([login_required, role_required(3)], name='dispatch')
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
