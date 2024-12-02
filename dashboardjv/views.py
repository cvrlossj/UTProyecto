from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
# Vistas Genericas
from django.views.generic import TemplateView, View
# Utilidades
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
import logging
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from dashboarda.utils import role_required
# Modelos de dashboarda
from dashboarda.models import JuntaVecinos
# Modelos de accounts
from accounts.models import Perfiles, Familia, EstadoPerfil, Sexo, Parentesco, Roles, Comuna
# Modelos propios
from django.db.models import Count
from django.db.models import Q
from .models import Noticias, CertificadosResi, EstadoNoticia, EstadoCertificado, Actividad, EstadoActividad, InscripcionActividad
# Email de Django
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# pdf
from django.utils.safestring import mark_safe
from io import BytesIO
from datetime import datetime
from smtplib import SMTPException 
from xhtml2pdf import pisa


# Configurar logging
logger = logging.getLogger(__name__)



#! ---- [Vecinos] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class ListaVecinosView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        vecinos = junta.perfiles.filter(id_rol=3)
        
        context = {
            'user': user,
            'junta': junta,
            'vecinos': vecinos,
        }
        return render(request, 'dashboardjv/listavecinos.html', context)
        

@method_decorator([login_required, role_required(2)], name='dispatch')
class CrearVecinoTitularView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        sexos = Sexo.objects.all()
        parentescos = Parentesco.objects.filter(id_parentesco=1)
        
        context = {
            'user': user,
            'junta': junta,
            'sexos': sexos,
            'parentescos': parentescos,
        }
        return render(request, 'dashboardjv/crearvecinotitular.html', context)
    
    def post(self, request, *args, **kwargs):
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        parentesco_id = request.POST.get('parentesco')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        fecha_incorporacion = request.POST.get('fecha_incorporacion')
        direccion = request.POST.get('direccion')
        contrasena = request.POST.get('contrasena')
        
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        if not all([rut, dv, nombre, apellido, fecha_nacimiento, sexo_id, numero_contacto, email, fecha_incorporacion, direccion, contrasena]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('dashboardjv:crearvecino')
        
        
        comuna_junta = junta.id_comuna  
        if not comuna_junta:
            messages.error(request, 'La junta de vecinos no tiene una comuna asignada.')
            return redirect('dashboardjv:crearvecino')
        
        try:
            # Obtener instancias de claves foráneas
            sexo = get_object_or_404(Sexo, id_sexo=sexo_id)
            parentesco = get_object_or_404(Parentesco, id_parentesco=parentesco_id)
            rol = get_object_or_404(Roles, id_rol=3)
            estado_perfil = get_object_or_404(EstadoPerfil, id_estadoperfil=1)
            
            vecino = Perfiles.objects.create(
                rut=rut,
                dv=dv,
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                id_sexo=sexo,
                id_parentesco=parentesco,
                numero_contacto=numero_contacto,
                correo_electronico=email,
                fecha_incorporacion=fecha_incorporacion,
                direccion=direccion,
                id_rol=rol,
                id_estadoperfil=estado_perfil,
                id_comuna=comuna_junta,
            )
            vecino.set_password(contrasena)
            vecino.save()
            junta.perfiles.add(vecino)
            
            if parentesco.descripcion == "Titular":
                familia = Familia.objects.create(
                    titular=vecino,
                    nombre=f"Familia {nombre} {apellido}",
                )
                vecino.familia = familia 
                vecino.save()
            else: 
                titular_familia = Perfiles.objects.filter(
                    id_parentesco__nombre="Titular",
                    id_comuna=comuna_junta
                ).first()
                if titular_familia and titular_familia.familia:
                    vecino.familia = titular_familia.familia
                    vecino.save()
                else:
                    messages.error(request, 'No se encontró un titular en la comuna para asociar a la familia.')
                    return redirect('dashboardjv:crearvecino')
            
            messages.success(request, f'El vecino {nombre} {apellido} ha sido creado exitosamente.')
            return redirect('dashboardjv:listavecinos')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear el vecino: {str(e)}')
            return redirect('dashboardjv:crearvecino')
        

@method_decorator([login_required, role_required(2)], name='dispatch')
class EditarVecinoTitular(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        vecino = get_object_or_404(Perfiles, rut=kwargs['rut'])
        sexos = Sexo.objects.all()
        estados_perfil = EstadoPerfil.objects.all()
        
        if vecino.id_parentesco.descripcion == "Titular":
            parentescos = Parentesco.objects.filter(id_parentesco=1)
        else:
            parentescos = Parentesco.objects.exclude(id_parentesco=1)
        
        context = {
            'user': user,
            'junta': junta,
            'vecino': vecino,
            'sexos': sexos,
            'parentescos': parentescos,
            'estados_perfil': estados_perfil,
        }
        return render(request, 'dashboardjv/editarvecinotitular.html', context)

    def post(self, request, *args, **kwargs):
        rut = kwargs['rut']
        vecino = get_object_or_404(Perfiles, rut=rut)
        
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        parentesco_id = request.POST.get('parentesco')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        contrasena = request.POST.get('contrasena')
        estado_id = request.POST.get('estado')
        fecha_termino = request.POST.get('fecha_termino')
        
        try:
            vecino.nombre = nombre
            vecino.apellido = apellido
            vecino.fecha_nacimiento = fecha_nacimiento
            vecino.id_sexo = get_object_or_404(Sexo, id_sexo=sexo_id)
            vecino.id_parentesco = get_object_or_404(Parentesco, id_parentesco=parentesco_id)
            vecino.numero_contacto = numero_contacto
            vecino.correo_electronico = email
            vecino.direccion = direccion
            vecino.id_estadoperfil = get_object_or_404(EstadoPerfil, id_estadoperfil=estado_id)  # Actualizar el estado
            if fecha_termino:
                vecino.fecha_termino = fecha_termino
            if contrasena: 
                vecino.set_password(contrasena)
            
            vecino.save()
            
            # Verificar si es titular y si el estado implica inhabilitación
            if vecino.id_parentesco.descripcion == "Titular" and vecino.fecha_termino:
                familia = vecino.familia
                if familia:
                    # Actualizar el estado y la fecha de término de todos los miembros
                    miembros = familia.miembros.all()
                    for miembro in miembros:
                        miembro.id_estadoperfil = vecino.id_estadoperfil
                        miembro.fecha_termino = vecino.fecha_termino
                        miembro.save()
            
            messages.success(request, 'El perfil del vecino se han actualizado correctamente.')
            return redirect('dashboardjv:listavecinos')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al actualizar el vecino: {str(e)}')
            return redirect('dashboardjv:editarvecino', rut=rut)

# ! ---- [Lista Miembros de una Familia] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class ListaMiembrosFamilia(View):
    def get(self, request, rut, *args, **kwargs):
        try:
            # Obtenemos el titular de la familia
            titular = get_object_or_404(Perfiles, rut=rut, id_parentesco__descripcion="Titular")
            
            familia = titular.familia
            
            if not familia:
                messages.error(request, 'El titular no tiene una familia asignada.')
                return redirect('dashboardjv:listavecinos')
            
            # Obtener todos los vecinos asociados a esta familia
            miembros = familia.miembros.all()
            miembros_contar = familia.miembros.all().count()
            
            context = { 
                'titular': titular,
                'familia': familia,
                'miembros': miembros,
                'miembros_contar': miembros_contar,
            }
            return render(request, 'dashboardjv/listamiembrosdetitulares.html', context)
        except Exception as e:
            messages.error(request, f'Ocurrió un error al obtener los miembros de la familia: {str(e)}')
            return redirect('dashboardjv:listavecinos')
        
        
@method_decorator(login_required, name='dispatch')
class CrearVecinoMiembroView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        sexos = Sexo.objects.all()
        parentescos = Parentesco.objects.exclude(id_parentesco=1) 
        
        titular_rut = kwargs.get('rut')
        titular = get_object_or_404(Perfiles, rut=titular_rut, id_parentesco__descripcion="Titular")
        
        context = {
            'user': user,
            'junta': junta,
            'sexos': sexos,
            'parentescos': parentescos,
            'titular': titular
        }
        return render(request, 'dashboardjv/crearvecinootro.html', context)
    
    def post(self, request, *args, **kwargs):
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        parentesco_id = request.POST.get('parentesco')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        fecha_incorporacion = request.POST.get('fecha_incorporacion')
        direccion = request.POST.get('direccion')
        # contrasena = request.POST.get('contrasena')
        
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        titular_rut = kwargs.get('rut')
        titular = get_object_or_404(Perfiles, rut=titular_rut, id_parentesco__descripcion="Titular")
        
        if not all([rut, dv, nombre, apellido, fecha_nacimiento, sexo_id, numero_contacto, email, fecha_incorporacion, direccion]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('dashboardjv:crear_miembro_familia', rut=titular_rut)
        
        try:
            sexo = get_object_or_404(Sexo, id_sexo=sexo_id)
            parentesco = get_object_or_404(Parentesco, id_parentesco=parentesco_id)
            rol = get_object_or_404(Roles, id_rol=3)
            estado_perfil = get_object_or_404(EstadoPerfil, id_estadoperfil=1)
            
            vecino = Perfiles.objects.create(
                rut=rut,
                dv=dv,
                nombre=nombre,
                apellido=apellido,
                fecha_nacimiento=fecha_nacimiento,
                id_sexo=sexo,
                id_parentesco=parentesco,
                numero_contacto=numero_contacto,
                correo_electronico=email,
                fecha_incorporacion=fecha_incorporacion,
                direccion=direccion,
                id_rol=rol,
                id_estadoperfil=estado_perfil,
                id_comuna=junta.id_comuna,
            )
            vecino.save()
            junta.perfiles.add(vecino)
            
            # Asociar a la familia del titular
            vecino.familia = titular.familia
            vecino.save()
            
            messages.success(request, f'El miembro {nombre} {apellido} ha sido creado exitosamente y asociado a la familia de {titular.nombre}.')
            return redirect('dashboardjv:lista_familia', rut=titular_rut)
        
        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear el miembro: {str(e)}')
            return redirect('dashboardjv:crear_miembro_familia', rut=titular_rut)


@method_decorator([login_required, role_required(2)], name='dispatch')
class EditarVecinoMiembroView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        vecino_rut = kwargs.get('rut')
        titular_rut = kwargs.get('titular_rut')
        estados_perfil = EstadoPerfil.objects.all()
        
        # Validar que el titular existe y pertenece a la junta
        titular = get_object_or_404(
            Perfiles,
            rut=titular_rut,
            id_parentesco__descripcion="Titular",
            familia__in=junta.perfiles.values_list('familia', flat=True)
        )
        
        # Validar que el vecino pertenece a la misma familia de la junta
        vecino = get_object_or_404(
            Perfiles,
            rut=vecino_rut,
            familia__in=junta.perfiles.values_list('familia', flat=True)
        )
        
        # Obtener sexos y parentescos
        sexos = Sexo.objects.all()
        
        if vecino.id_parentesco.descripcion == "Titular":
            parentescos = Parentesco.objects.filter(id_parentesco=1)
        else:
            parentescos = Parentesco.objects.exclude(id_parentesco=1)
        
        context = {
            'user': user,
            'junta': junta,
            'titular': titular,
            'vecino': vecino,
            'sexos': sexos,
            'parentescos': parentescos,
            'estados_perfil': estados_perfil,
        }
        return render(request, 'dashboardjv/editarvecinootro.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        vecino_rut = kwargs.get('rut')
        titular_rut = kwargs.get('titular_rut')
        
        titular = get_object_or_404(
            Perfiles,
            rut=titular_rut,
            id_parentesco__descripcion="Titular",
            familia__in=junta.perfiles.values_list('familia', flat=True)
        )
        
        # Validar que el vecino pertenece a la misma familia de la junta
        vecino = get_object_or_404(
            Perfiles,
            rut=vecino_rut,
            familia__in=junta.perfiles.values_list('familia', flat=True)
        )
        
        # Capturar datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        parentesco_id = request.POST.get('parentesco')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        estado_id = request.POST.get('estado')
        fecha_termino = request.POST.get('fecha_termino')

        # Validar y guardar cambios
        try:
            vecino.nombre = nombre
            vecino.apellido = apellido
            vecino.fecha_nacimiento = fecha_nacimiento
            vecino.id_sexo_id = sexo_id
            vecino.id_parentesco_id = parentesco_id
            vecino.numero_contacto = numero_contacto
            vecino.correo_electronico = email
            vecino.direccion = direccion
            vecino.id_estadoperfil_id = estado_id
            if fecha_termino:
                vecino.fecha_termino = fecha_termino
            vecino.save()
            # Mensaje de éxito
            messages.success(request, "El miembro fue actualizado exitosamente.")
            return redirect('dashboardjv:lista_familia', titular_rut)
        except Exception as e:
            # Mensaje de error
            messages.error(request, f"Hubo un error al actualizar el miembro: {str(e)}")
            return redirect('dashboardjv:editar_miembro_familia', titular_rut=titular_rut, rut=vecino_rut)

# ! ---- [Final de Familia] ----
        
#! ---- [Noticias] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class ListaNoticias(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        noticias = Noticias.objects.filter(id_juntavecinos=junta)
        
        context = {
            'user': user,
            'junta': junta,
            'noticias': noticias,
        }
        return render(request, 'dashboardjv/listanoticias.html', context)

@method_decorator([login_required, role_required(2)], name='dispatch')
class CrearNoticia(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        total_miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1).count()
        
        context = {
            'user': user,
            'junta': junta,
            'total_miembros': total_miembros
        }
        return render(request, 'dashboardjv/crearnoticia.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino', None)
        
        if titulo and descripcion and fecha_inicio:
            try:
                estado = EstadoNoticia.objects.get(pk=1)
                noticia = Noticias.objects.create(
                    nombre=titulo,
                    descripcion=descripcion,
                    fecha_inicio=fecha_inicio,
                    fecha_termino=fecha_termino,
                    id_estadonoticia=estado,
                    id_juntavecinos=junta
                )

                miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1)
                correos = [miembro.correo_electronico for miembro in miembros if miembro.correo_electronico]

                if correos:
                    try:
                        # Crear el contenido HTML
                        html_content = f"""
                        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                            <div style="background-color: #007bff; color: white; padding: 20px; text-align: center;">
                                <h1 style="margin: 0;">{junta.nombre_organizacion}</h1>
                                <p style="margin: 10px 0 0 0;">Nueva Noticia</p>
                            </div>
                            
                            <div style="padding: 20px; background-color: #f8f9fa;">
                                <h2 style="color: #007bff;">{noticia.nombre}</h2>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                                    <p><strong>Fecha de publicación:</strong> {noticia.fecha_inicio}</p>
                                </div>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px;">
                                    {noticia.descripcion}
                                </div>
                                
                                <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 0.9em;">
                                    <p>Este es un mensaje automático de tu Junta de Vecinos</p>
                                    <p>Por favor, no responder a este correo</p>
                                </div>
                            </div>
                        </div>
                        """

                        text_content = f"""
                        {junta.nombre_organizacion}
                        Nueva Noticia

                        {noticia.nombre}

                        Fecha publicación : {noticia.fecha_inicio}

                        {noticia.descripcion}

                        Este es un mensaje automático de tu Junta de Vecinos
                        Por favor, no responder a este correo
                        """

                        subject = f"Nueva noticia: {noticia.nombre}"
                        for correo in correos:
                            email = EmailMultiAlternatives(
                                subject=subject,
                                body=text_content,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[correo] 
                            )
                            email.attach_alternative(html_content, "text/html")
                            email.send()

                        messages.success(request, "Noticia creada y enviada exitosamente.")

                    except Exception as e:
                        logger.error(f"Error al enviar el correo: {str(e)}")
                        messages.warning(request, "La noticia se creó pero hubo un error al enviar los correos.")

                return redirect('dashboardjv:listanoticias')

            except Exception as e:
                logger.error(f"Error al crear la noticia: {str(e)}")
                messages.error(request, f'Error al crear la noticia: {str(e)}')
                context = {
                    'user': user,
                    'junta': junta,
                }
                return render(request, 'dashboardjv/crearnoticia.html', context)
        else:
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            context = {
                'user': user,
                'junta': junta,
            }
            return render(request, 'dashboardjv/crearnoticia.html', context)



@method_decorator([login_required, role_required(2)], name='dispatch')
class EditarNoticia(View):
    def get(self, request, id_noticia, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        noticia = get_object_or_404(Noticias, id_noticia=id_noticia, id_juntavecinos=junta)
        total_miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1).count()
        estado_noticia = EstadoNoticia.objects.all()
        
        context = {
            'user': user,
            'junta': junta,
            'noticia': noticia,
            'total_miembros': total_miembros,
            'estados': estado_noticia
        }
        return render(request, 'dashboardjv/editarnoticia.html', context)
    
    def post(self, request, id_noticia, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        noticia = get_object_or_404(Noticias, id_noticia=id_noticia, id_juntavecinos=junta)
        
        # Obtener los elementos del html
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')  
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_termino = request.POST.get('fecha_termino', None)
        estado = request.POST.get('estado')
        
        if titulo and descripcion and fecha_inicio:
            try:
                noticia.nombre = titulo
                noticia.descripcion = descripcion
                if fecha_inicio:
                    noticia.fecha_inicio = fecha_inicio
                if fecha_termino:
                    noticia.fecha_termino = fecha_termino
                noticia.fecha_termino = fecha_termino
                noticia.id_estadonoticia = EstadoNoticia.objects.get(pk=estado)
                noticia.save()
                
                miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1)
                correos = [miembro.correo_electronico for miembro in miembros if miembro.correo_electronico]
                
        
                if correos:
                    try:
                        html_content = f"""
                        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                            <div style="background-color: #007bff; color: white; padding: 20px; text-align: center;">
                                <h1 style="margin: 0;">{junta.nombre_organizacion}</h1>
                                <p style="margin: 10px 0 0 0;">Edición de Noticia</p>
                            </div>
                            
                            <div style="padding: 20px; background-color: #f8f9fa;">
                                <h2 style="color: #007bff;">{noticia.nombre}</h2>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                                    <p><strong>Fecha de modificación:</strong> {noticia.fecha_inicio}</p>
                                </div>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px;">
                                    {noticia.descripcion}
                                </div>
                                
                                <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 0.9em;">
                                    <p>Este es un mensaje automático de tu Junta de Vecinos</p>
                                    <p>Por favor, no responder a este correo</p>
                                </div>
                            </div>
                        </div>
                        """

                        text_content = f"""
                        {junta.nombre_organizacion}
                        Edición de Noticia

                        {noticia.nombre}

                        Fecha de modificación: {noticia.fecha_inicio}

                        {noticia.descripcion}

                        Este es un mensaje automático de tu Junta de Vecinos
                        Por favor, no responder a este correo
                        """

                        subject = f"Noticia editada: {noticia.nombre}"
                        for correo in correos:
                            email = EmailMultiAlternatives(
                                subject=subject,
                                body=text_content,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[correo]
                            )
                            email.attach_alternative(html_content, "text/html")
                            email.send()

                        messages.success(request, "Noticia editada y notificación enviada exitosamente.")

                    except Exception as e:
                        logger.error(f"Error al enviar el correo: {str(e)}")
                        messages.warning(request, "La noticia se editó pero hubo un error al enviar los correos.")

                return redirect('dashboardjv:listanoticias')
        
            except Exception as e:
                logger.error(f"Error al crear la noticia: {str(e)}")
                messages.error(request, f'Error al crear la noticia: {str(e)}')
                context = {
                    'user': user,
                    'junta': junta,
                }
                return render(request, 'dashboardjv/editarnoticia.html', context)
        
        else:
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')

        context = {
            'user': user,
            'junta': junta,
            'noticia': noticia,
        }
        return render(request, 'dashboardjv/editarnoticia.html', context)
        
#! ---- [Final de Noticias]


#! ---- [Certificado de Residencia] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class ListaCertificados(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        certificados = CertificadosResi.objects.filter(id_juntavecinos=junta)
        
        context = {
            'user': user,
            'junta': junta,
            'certificados': certificados,
        }
        return render(request, 'dashboardjv/certificados/listacertificados.html', context)


@method_decorator([login_required, role_required(2)], name='dispatch')
class CrearCertificado(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        certificados = CertificadosResi.objects.filter(id_juntavecinos=junta)
        
        context = {
            'user': user,
            'junta': junta,
            'certificados': certificados,
        }
        return render(request, 'dashboardjv/certificados/crearcertificado.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        # Formulario
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')

        if not (rut and nombre and email and direccion):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('dashboardjv:crearcertificado')

        try:
            estado_certificado = get_object_or_404(EstadoCertificado, id_estadocertificado=2)

            certificado = CertificadosResi.objects.create(
                nombre_postulante=nombre,
                direccion_postulante=direccion,
                fecha_emision=datetime.now(),
                id_juntavecinos=junta,
                rut_postulante=get_object_or_404(Perfiles, rut=rut),
                id_estadocertificado=estado_certificado
            )

            # HTML del certificado
            html_content = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Certificado de Residencia</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        font-size: 14px;
                    }}
                    .header {{
                        text-align: center;
                        background-color: #007bff;
                        color: white;
                        padding: 20px;
                    }}
                    .content {{
                        margin: 20px;
                    }}
                    .footer {{
                        text-align: center;
                        font-size: 12px;
                        margin-top: 20px;
                        color: #6c757d;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{junta.nombre_organizacion}</h1>
                </div>
                <div class="content">
                    <p>A quien corresponda:</p>
                    
                    <p>Por medio del presente, la Junta de Vecinos <strong>{junta.nombre_organizacion}</strong> certifica que:</p>
                    
                    <p>El vecino <strong>{nombre} {apellido}</strong> con RUT <strong>{rut}</strong> con dirección domiciliaria en <strong>{direccion}</strong> reside en esta dirección que hace constancia en nuestros registros.</p>
                    
                    <p>Este certificado se emite en <strong>{junta.direccion}</strong> el día <strong>{certificado.fecha_emision.strftime("%d/%m/%Y")}</strong></p>
                    
                    <br>
                    <p>Atentamente,</p>
                    <p><strong>Junta de Vecinos {junta.nombre_organizacion}</strong></p>
                </div>
                <div class="footer">
                    <p>Documento generado automáticamente por la Junta de Vecinos</p>
                </div>
            </body>
            </html>
            """

            # Generar el PDF
            pdf = BytesIO()
            pisa_status = pisa.CreatePDF(html_content, dest=pdf)

            if pisa_status.err:
                logger.error("Error al generar el PDF")
                messages.error(request, "Hubo un error al generar el certificado.")
                return redirect('dashboardjv:crearcertificado')

            # Guardar una copia del contenido del PDF
            pdf_content = pdf.getvalue()
            pdf.close()

            # Enviar el correo electrónico
            try:
                subject = "Certificado de Residencia"
                message = f"""
                Estimado/a {nombre} {apellido},

                Adjunto encontrará su certificado de residencia solicitado a la Junta de Vecinos {junta.nombre_organizacion}.

                Este es un correo automático, por favor no responder.

                Saludos cordiales,
                Junta de Vecinos {junta.nombre_organizacion}
                """
                
                email_message = EmailMultiAlternatives(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                email_message.attach(
                    f"certificado_{certificado.id_certificado}.pdf",
                    pdf_content,
                    "application/pdf"
                )
                email_message.send()
                
                messages.success(
                    request, 
                    mark_safe(
                        f"Certificado #{certificado.id_certificado} generado y enviado correctamente al correo "
                        f"<strong>{email}</strong>"
                    )
                )

            except SMTPException as e:
                logger.error(f"Error SMTP al enviar el correo: {str(e)}")
                messages.error(
                    request, 
                    "Hubo un error al enviar el certificado por correo. Por favor, inténtelo nuevamente."
                )
                certificado.delete()
                return redirect('dashboardjv:crearcertificado')
                
            except Exception as e:
                logger.error(f"Error inesperado al enviar el correo: {str(e)}")
                messages.error(
                    request, 
                    "Ocurrió un error inesperado. Por favor, inténtelo nuevamente."
                )
                certificado.delete()
                return redirect('dashboardjv:crearcertificado')

            return redirect('dashboardjv:listacertificados')

        except Exception as e:
            logger.exception("Error al crear el certificado:")
            messages.error(request, f"Hubo un error al procesar el certificado: {str(e)}")
            return redirect('dashboardjv:crearcertificado')


@method_decorator([login_required, role_required(2)], name='dispatch')
class EditarCertificado(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        certificado = get_object_or_404(CertificadosResi, id_certificado=kwargs['id_certificado'], id_juntavecinos=junta)
        estados = EstadoCertificado.objects.exclude(id_estadocertificado=2)
        
        context = {
            'user': user,
            'junta': junta,
            'certificado': certificado,
            'estados': estados,
        }
        return render(request, 'dashboardjv/certificados/editarcertificado.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        certificado = get_object_or_404(CertificadosResi, id_certificado=kwargs['id_certificado'], id_juntavecinos=junta)
        
        estado_id = request.POST.get('estado')
        razon_rechazo = request.POST.get('nota', '')

        if not estado_id:
            messages.error(request, 'Debe seleccionar un estado para continuar.')
            return redirect('dashboardjv:editarcertificado', id_certificado=certificado.id_certificado)

        try:
            nuevo_estado = get_object_or_404(EstadoCertificado, id_estadocertificado=estado_id)
            certificado.id_estadocertificado = nuevo_estado
            
            certificado.fecha_emision = datetime.now().date()

            if nuevo_estado.descripcion.lower() == 'aprobar':
                estado_emitido = get_object_or_404(EstadoCertificado, id_estadocertificado=2)
                certificado.id_estadocertificado = estado_emitido

                html_content = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <title>Certificado de Residencia</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            font-size: 14px;
                        }}
                        .header {{
                            text-align: center;
                            background-color: #007bff;
                            color: white;
                            padding: 20px;
                        }}
                        .content {{
                            margin: 20px;
                        }}
                        .footer {{
                            text-align: center;
                            font-size: 12px;
                            margin-top: 20px;
                            color: #6c757d;
                        }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>{junta.nombre_organizacion}</h1>
                    </div>
                    <div class="content">
                        <p>A quien corresponda:</p>
                        
                        <p>Por medio del presente, la Junta de Vecinos <strong>{junta.nombre_organizacion}</strong> certifica que:</p>
                        
                        <p>El vecino <strong>{certificado.nombre_postulante} {certificado.rut_postulante.apellido}</strong> con RUT <strong>{certificado.rut_postulante.rut}</strong> con dirección domiciliaria en <strong>{certificado.direccion_postulante}</strong> reside en esta dirección que hace constancia en nuestros registros.</p>
                        
                        <p>Este certificado se emite en <strong>{junta.direccion}</strong> el día <strong>{datetime.now().strftime("%d/%m/%Y")}</strong></p>
                        
                        <br>
                        <p>Atentamente,</p>
                        <p><strong>Junta de Vecinos {junta.nombre_organizacion}</strong></p>
                    </div>
                    <div class="footer">
                        <p>Documento generado automáticamente por la Junta de Vecinos</p>
                    </div>
                </body>
                </html>
                """

                pdf = BytesIO()
                pisa_status = pisa.CreatePDF(html_content, dest=pdf)

                if pisa_status.err:
                    logger.error("Error al generar el PDF")
                    messages.error(request, "Hubo un error al generar el certificado.")
                    return redirect('dashboardjv:editarcertificado', id_certificado=certificado.id_certificado)

                pdf_content = pdf.getvalue()
                pdf.close()

                # Enviar el correo con el certificado aprobado
                subject = "Certificado de Residencia Aprobado"
                message = f"""
                Estimado/a {certificado.nombre_postulante} {certificado.rut_postulante.apellido},

                Su certificado de residencia ha sido aprobado. Adjunto encontrará el documento oficial.

                Saludos cordiales,
                Junta de Vecinos {junta.nombre_organizacion}
                """
                email_message = EmailMultiAlternatives(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [certificado.rut_postulante.correo_electronico]
                )
                email_message.attach(f"certificado_{certificado.id_certificado}.pdf", pdf_content, "application/pdf")
                email_message.send()

            elif nuevo_estado.descripcion.lower() == 'rechazar':
                # Guardar la razón de rechazo
                certificado.nota_estado = razon_rechazo

                # Enviar correo de rechazo
                subject = "Certificado de Residencia Rechazado"
                message = f"""
                Estimado/a {certificado.nombre_postulante} {certificado.rut_postulante.apellido},

                Lamentamos informarle que su solicitud de certificado de residencia ha sido rechazada por la siguiente razón:

                "{razon_rechazo}"

                Para más información, puede contactar a la Junta de Vecinos {junta.nombre_organizacion}.
                """
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [certificado.rut_postulante.correo_electronico]
                )

            certificado.save()
            messages.success(request, f"El estado del certificado #{certificado.id_certificado} se actualizó correctamente.")
            return redirect('dashboardjv:listacertificados')

        except Exception as e:
            logger.exception("Error al editar el certificado:")
            messages.error(request, f"Hubo un error al editar el certificado: {str(e)}")
            return redirect('dashboardjv:editarcertificado', id_certificado=certificado.id_certificado)




@csrf_exempt
@login_required
def vecinos_chart_data(request):
    if request.method == 'GET':
        try:
            # Obtener la junta de vecinos asociada al usuario actual
            user = request.user
            try:
                junta = JuntaVecinos.objects.get(perfiles=user)
            except JuntaVecinos.DoesNotExist:
                return JsonResponse({'error': 'No estás asociado a ninguna junta de vecinos.'}, status=400)

            today = datetime.now().date()
            # Obtener primer día del mes actual
            first_day = today.replace(day=1)
            # Obtener último día del mes
            if today.month == 12:
                last_day = today.replace(day=31)
            else:
                last_day = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            # Generar datos para cada día del mes
            labels = []
            integrados_count = []
            inhabilitados_count = []

            current_day = first_day
            while current_day <= last_day:
                labels.append(current_day.strftime('%d/%m'))

                # Contar vecinos integrados por día
                integrados = junta.perfiles.filter(id_rol=3, fecha_incorporacion=current_day).count()
                integrados_count.append(integrados)

                # Contar vecinos inhabilitados por día
                inhabilitados = junta.perfiles.filter(id_rol=3, fecha_termino=current_day).count()
                inhabilitados_count.append(inhabilitados)

                current_day += timedelta(days=1)

            return JsonResponse({
                'labels': labels,
                'integrados': integrados_count,
                'inhabilitados': inhabilitados_count
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
@login_required
def filter_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filter_type = data.get('filter_type')
            filter_value = data.get('filter_value')

            # Obtener la junta de vecinos asociada al usuario actual
            user = request.user
            try:
                junta = JuntaVecinos.objects.get(perfiles=user)
            except JuntaVecinos.DoesNotExist:
                return JsonResponse({'error': 'No estás asociado a ninguna junta de vecinos.'}, status=400)

            # Inicializamos los valores en 0
            total_vecinos = 0
            total_vecinos_habilitados = 0
            total_vecinos_inhabilitados = 0

            # Crear filtros de fecha según el filtro proporcionado
            if filter_value == 'today':
                date_filter = datetime.now().date()
                date_query = Q(fecha_incorporacion=date_filter)
            elif filter_value == 'week':
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                date_query = Q(fecha_incorporacion__gte=week_start)
            elif filter_value == 'month':
                month_start = datetime.now().replace(day=1)
                date_query = Q(fecha_incorporacion__gte=month_start)
            elif filter_value == 'year':
                year_start = datetime.now().replace(month=1, day=1)
                date_query = Q(fecha_incorporacion__gte=year_start)
            else:
                date_query = Q()

            # Aplicar filtros según el tipo
            if filter_type == 'total':
                total_vecinos = junta.perfiles.filter(Q(id_rol=3) & date_query).count()
            elif filter_type == 'habilitadas':
                total_vecinos_habilitados = junta.perfiles.filter(Q(id_rol=3, id_estadoperfil=1) & date_query).count()
            elif filter_type == 'inhabilitadas':
                total_vecinos_inhabilitados = junta.perfiles.filter(Q(id_rol=3, id_estadoperfil=2) & date_query).count()


            # Respuesta JSON con los datos filtrados
            return JsonResponse({
                'total_vecinos': total_vecinos,
                'total_vecinos_habilitados': total_vecinos_habilitados,
                'total_vecinos_inhabilitados': total_vecinos_inhabilitados
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método de solicitud inválido.'}, status=405)


@csrf_exempt
@login_required
def reset_data(request):
    if request.method == 'POST':
        try:
            # Obtener la junta de vecinos asociada al usuario actual
            user = request.user
            try:
                junta = JuntaVecinos.objects.get(perfiles=user)
            except JuntaVecinos.DoesNotExist:
                return JsonResponse({'error': 'No estás asociado a ninguna junta de vecinos.'}, status=400)

            # Obtener totales para la junta específica
            total_vecinos = junta.perfiles.filter(id_rol=3).count()
            habilitados_vecinos = junta.perfiles.filter(id_rol=3, id_estadoperfil=1).count()
            inhabilitados_vecinos = junta.perfiles.filter(id_rol=3, id_estadoperfil=2).count()

            # Respuesta JSON
            return JsonResponse({
                'total_vecinos': total_vecinos,
                'habilitados_vecinos': habilitados_vecinos,
                'inhabilitados_vecinos': inhabilitados_vecinos
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# ! ---- [Final de Certificado de Residencia]


#! ---- [Actividades] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class ListaActividades(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        actividades = Actividad.objects.filter(id_juntavecinos=junta)
        
        # Contar cu[antos cupos han sido tomados para cada actividad
        for actividad in actividades:
            actividad.cupos_tomados = InscripcionActividad.objects.filter(id_actividad=actividad).count()
        
        context = {
            'user': user,
            'junta': junta,
            'actividades': actividades,
        }
        return render(request, 'dashboardjv/actividades/listaactividades.html', context)


@method_decorator([login_required, role_required(2)], name='dispatch')
class CrearActividad(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        actividades = Actividad.objects.filter(id_juntavecinos=junta)
        total_miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1).count()
        
        context = {
            'user': user,
            'junta': junta,
            'actividades': actividades,
            'total_miembros': total_miembros
        }
        return render(request, 'dashboardjv/actividades/crearactividad.html', context)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        # Formulario
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inc = request.POST.get('fecha_inc')
        hora_inc = request.POST.get('hora_inc')
        hora_ter = request.POST.get('hora_ter')
        cupos = request.POST.get('cupos')
        
        if titulo and descripcion and fecha_inc and hora_inc and hora_ter and cupos:
            try:
                # Creamos la actividad
                estado = EstadoActividad.objects.get(pk=1) 
                actividad = Actividad.objects.create(
                    nombre=titulo,
                    descripcion=descripcion,
                    fecha_inicio=fecha_inc,
                    horario_inicio=hora_inc,
                    horario_termino=hora_ter,
                    cupos=cupos,
                    id_estadoactividad=estado,
                    id_juntavecinos=junta
                )

                # Obtener los correos electrónicos de los miembros activos
                miembros = junta.perfiles.filter(id_rol=3, id_estadoperfil=1)  # Miembros activos
                correos = [miembro.correo_electronico for miembro in miembros if miembro.correo_electronico]

                if correos:
                    try:
                        # Crear el contenido HTML
                        html_content = f"""
                        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                            <div style="background-color: #007bff; color: white; padding: 20px; text-align: center;">
                                <h1 style="margin: 0;">{junta.nombre_organizacion}</h1>
                                <p style="margin: 10px 0 0 0;">Nueva Actividad</p>
                            </div>
                            
                            <div style="padding: 20px; background-color: #f8f9fa;">
                                <h2 style="color: #007bff;">{actividad.nombre}</h2>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                                    <p><strong>Fecha de Actividad:</strong> {actividad.fecha_inicio}</p>
                                    <p><strong>Hora inicio:</strong> {actividad.horario_inicio}</p>
                                    <p><strong>Hora término:</strong> {actividad.horario_termino}</p>
                                    <p><strong>Cupos disponibles:</strong> {actividad.cupos}</p>
                                </div>
                                
                                <div style="background-color: white; padding: 15px; border-radius: 5px;">
                                    {actividad.descripcion}
                                </div>
                                
                                <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 0.9em;">
                                    <p>Este es un mensaje automático de tu Junta de Vecinos</p>
                                    <p>Por favor, no responder a este correo</p>
                                </div>
                            </div>
                        </div>
                        """

                        text_content = f"""
                        {junta.nombre_organizacion}
                        Nueva Actividad

                        {actividad.nombre}

                        Fecha inicio: {actividad.fecha_inicio}
                        Hora inicio: {actividad.horario_inicio}
                        Hora término: {actividad.horario_termino}
                        Cupos disponibles: {actividad.cupos}

                        {actividad.descripcion}

                        Este es un mensaje automático de tu Junta de Vecinos
                        Por favor, no responder a este correo
                        """

                        subject = f"Nueva Actividad: {actividad.nombre}"
                        for correo in correos:
                            email = EmailMultiAlternatives(
                                subject=subject,
                                body=text_content,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[correo] 
                            )
                            email.attach_alternative(html_content, "text/html")
                            email.send()

                        messages.success(request, "Actividad creada y enviada exitosamente.")

                    except Exception as e:
                        logger.error(f"Error al enviar el correo: {str(e)}")
                        messages.warning(request, "La actividad se creó pero hubo un error al enviar los correos.")

                return redirect('dashboardjv:listaactividades')  # Asegúrate de que esta URL sea correcta

            except Exception as e:
                logger.error(f"Error al crear la actividad: {str(e)}")
                messages.error(request, f'Error al crear la actividad: {str(e)}')
                context = {
                    'user': user,
                    'junta': junta,
                }
                return render(request, 'dashboardjv/actividades/crearactividad.html', context)
        else:
            messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            context = {
                'user': user,
                'junta': junta,
            }
            return render(request, 'dashboardjv/actividades/crearactividad.html', context)
        

#! ---- [Dashboard Junta de Vecinos] ----
@method_decorator([login_required, role_required(2)], name='dispatch')
class DashboardJuntaVecino(TemplateView):
    template_name = "dashboardjv/dashboardjuntavecino.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        junta = get_object_or_404(JuntaVecinos, perfiles=user)
        
        total_vecinos = junta.perfiles.filter(id_rol=3).count()
        total_vecinos_habilitados = junta.perfiles.filter(id_rol=3, id_estadoperfil=1).count()
        total_vecinos_inhabilitados = junta.perfiles.filter(id_rol=3, id_estadoperfil=2).count()


        context.update({
            'user': user,
            'junta': junta,
            'total_vecinos' : total_vecinos,
            'total_vecinos_habilitados' : total_vecinos_habilitados,
            'total_vecinos_inhabilitados' : total_vecinos_inhabilitados,
        })
        return context
    

