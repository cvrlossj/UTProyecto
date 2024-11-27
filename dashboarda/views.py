from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
# Vistas Genericas
from django.views.generic import TemplateView, View
# Utilidades
from .utils import role_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Modelos
from accounts.models import Comuna, Perfiles, Sexo, Region, Comuna, Roles, EstadoPerfil
from .models import JuntaVecinos, EstadoJuntaVecinos
from django.db.models import Q, Count, Prefetch
# Mensajes
from django.contrib import messages



def acceso_denegado(request):
    return render(request, 'dashboarda/access_denied.html')


def obtener_juntas_vecinos(request):
    juntas = JuntaVecinos.objects.all()
    data = [
        {
            "nombre": junta.nombre_organizacion,
            "direccion": junta.direccion,
            "latitud": junta.latitud,
            "longitud": junta.longitud,
            "estado_id": junta.id_estado.id_estado,  # Aquí obtenemos el estado
        }
        for junta in juntas if junta.latitud and junta.longitud
    ]
    return JsonResponse(data, safe=False)

# Cargar Perfiles por Comuna
def get_perfiles_by_comuna(request, comuna_id):
    perfiles = Perfiles.objects.filter(id_comuna=comuna_id, id_rol=2, id_estadoperfil=1).exclude(juntavecinos__isnull=False)
    perfiles_list = list(perfiles.values('rut', 'nombre', 'apellido'))
    return JsonResponse(perfiles_list, safe=False)

# Cargar comunas
def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(id_region=region_id).order_by('nombre_comuna')
    comunas_list = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas]
    return JsonResponse(comunas_list, safe=False)


@csrf_exempt
def juntas_por_region_chart_data(request):
    today = now().date()  # Obtener la fecha actual
    last_7_days = today - timedelta(days=7)  # Usar timedelta para restar días

    juntas_por_region = (
        JuntaVecinos.objects
        .filter(fecha_integracion__range=(last_7_days, today))  # Filtrar por los últimos 7 días
        .values('id_comuna__id_region__nombre_region')  # Acceder al nombre de la región
        .annotate(count=Count('id_juntavecino'))  # Contar por la clave primaria
        .order_by('id_comuna__id_region__nombre_region')  # Ordenar por región
    )

    labels = [item['id_comuna__id_region__nombre_region'] for item in juntas_por_region]
    data = [item['count'] for item in juntas_por_region]

    return JsonResponse({
        'labels': labels,
        'data': data
    })


@csrf_exempt
def juntas_chart_data(request):
    if request.method == 'GET':
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
        integradas_count = []
        inhabilitadas_count = []

        current_day = first_day
        while current_day <= last_day:
            labels.append(current_day.strftime('%d/%m'))

            # Contar Juntas integradas por día
            integradas = JuntaVecinos.objects.filter(fecha_integracion=current_day).count()
            integradas_count.append(integradas)

            # Contar Juntas inhabilitadas por día
            inhabilitadas = JuntaVecinos.objects.filter(fecha_termino=current_day).count()
            inhabilitadas_count.append(inhabilitadas)

            current_day += timedelta(days=1)

        return JsonResponse({
            'labels': labels,
            'integradas': integradas_count,
            'inhabilitadas': inhabilitadas_count
        })


@method_decorator([login_required, role_required(1)], name='dispatch')
class PerfilesVecinosView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        perfiles = Perfiles.objects.filter(id_rol=2).select_related('id_comuna', 'id_comuna__id_region').prefetch_related(
            Prefetch('juntavecinos_set', queryset=JuntaVecinos.objects.select_related('id_comuna'))
        ).all()
        
        context = {
            'user': user,
            'perfiles': perfiles,
        }
        return render(request, 'dashboarda/perfilesasociados.html', context)


@method_decorator([login_required, role_required(1)], name='dispatch')
class CrearPerfilVecinoView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        sexos = Sexo.objects.all()
        regiones = Region.objects.all()
        comunas = Region.objects.first().comuna_set.all()
        
        context = {
            'user': user,
            'sexos': sexos,
            'regiones': regiones,
            'comunas': comunas,
        }
        return render(request, 'dashboarda/crearperfil.html', context)
    
    def post(self, request, *args, **kwargs):
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        fecha_incorporacion = request.POST.get('fecha_incorporacion')
        region_id = request.POST.get('region')
        comuna_id = request.POST.get('comuna')
        contrasena = request.POST.get('contrasena')

        if not all([rut, dv, nombre, apellido, sexo_id, numero_contacto, email, fecha_incorporacion, region_id, comuna_id, contrasena]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('dashboarda:crear_perfil')

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            fecha_incorporacion = datetime.strptime(fecha_incorporacion, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
            return redirect('dashboarda:crear_perfil')
        
        # Obtener objetos relacionados
        try:
            sexo = Sexo.objects.get(id_sexo=sexo_id)
            comuna = Comuna.objects.get(id_comuna=comuna_id)
            rol = Roles.objects.get(id_rol=2)
        except (Sexo.DoesNotExist, Comuna.DoesNotExist, Roles.DoesNotExist):
            messages.error(request, 'Sexo, Comuna o Rol no encontrados.')
            return redirect('dashboarda:crear_perfil')

        perfil = Perfiles(
            rut=rut,
            dv=dv,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            id_sexo=sexo,
            numero_contacto=numero_contacto,
            correo_electronico=email,
            fecha_incorporacion=fecha_incorporacion,
            id_comuna=comuna,
            id_rol=rol
        )
        perfil.set_password(contrasena)
        perfil.save()

        messages.success(request, 'Perfil creado exitosamente.')
        return redirect('dashboarda:perfiles')

@method_decorator([login_required, role_required(1)], name='dispatch')
class EditarPerfilVecinoView(View):
    def get(self, request, *args, **kwargs):
        rut = kwargs.get('rut')
        perfil = get_object_or_404(Perfiles, rut=rut)
        junta = perfil.juntavecinos_set.first()
        sexos = Sexo.objects.all()
        regiones = Region.objects.all()
        estado_perfil = EstadoPerfil.objects.all()
        comunas = perfil.id_comuna.id_region.comuna_set.all()
        perfil.refresh_from_db()
        # Convertir fechas al formato `yyyy-MM-dd`
        fecha_nacimiento = perfil.fecha_nacimiento.strftime('%Y-%m-%d') if perfil.fecha_nacimiento else ''
        fecha_incorporacion = perfil.fecha_incorporacion.strftime('%Y-%m-%d') if perfil.fecha_incorporacion else ''
        
        context = {
            'perfil': perfil,
            'sexos': sexos,
            'regiones': regiones,
            'comunas': comunas,
            'estados': estado_perfil,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_incorporacion': fecha_incorporacion,
            'junta': junta
        }
        return render(request, 'dashboarda/editarperfil.html', context)

    def post(self, request, *args, **kwargs):
        rut = kwargs.get('rut')
        perfil = Perfiles.objects.get(rut=rut)
        
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo_id = request.POST.get('sexo')
        numero_contacto = request.POST.get('numero_contacto')
        email = request.POST.get('email')
        comuna_id = request.POST.get('comuna')
        contrasena = request.POST.get('contrasena')
        estado_perfil_id = request.POST.get('estado_perfil')
        fecha_termino = request.POST.get('fecha_termino')
        
        
        # Validaciones
        if not all([nombre, apellido, fecha_nacimiento, sexo_id, numero_contacto, email, comuna_id, estado_perfil_id]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('dashboarda:editar_perfil_junta', rut=rut)
        
        perfil.nombre = nombre
        perfil.apellido = apellido
        perfil.fecha_nacimiento = fecha_nacimiento
        perfil.id_sexo_id = sexo_id
        perfil.numero_contacto = numero_contacto
        perfil.correo_electronico = email
        perfil.id_comuna_id = comuna_id
        if contrasena:
            perfil.set_password(contrasena)
            
        # Validar y asignar estado del perfil
        # try:
        #     estado_perfil = EstadoPerfil.objects.get(pk=estado_perfil_id)
        #     perfil.id_estadoperfil = estado_perfil
        # except EstadoPerfil.DoesNotExist:
        #     messages.error(request, "El estado seleccionado no es válido.")
        #     return redirect('dashboarda:editar_perfil_junta', rut=rut)
        perfil.id_estadoperfil_id = estado_perfil_id
        if fecha_termino:
            perfil.fecha_termino = fecha_termino
        else:
            perfil.fecha_termino = None
        perfil.save()
        messages.success(request, "Perfil actualizado con éxito.")
        return redirect('dashboarda:perfiles')


@method_decorator([login_required, role_required(1)], name='dispatch')
class CrearJuntaVecinosView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        sexos = Sexo.objects.all()
        regiones = Region.objects.all()
        comunas = Region.objects.first().comuna_set.all()
        estados = EstadoJuntaVecinos.objects.all()
        
        context = {
            'user': user,
            'sexos': sexos,
            'regiones': regiones,
            'comunas': comunas,
            'estados': estados,
        }
        return render(request, 'dashboarda/crearjuntavecino.html', context)
    
    def post(self, request, *args, **kwargs):
        try:
            nombre_organizacion = request.POST.get('nombreOrganizacion')
            fecha_integracion = request.POST.get('fechaIntegracion')
            comuna_id = request.POST.get('comuna')
            direccion = request.POST.get('direccionOrganizacion')
            perfiles_seleccionados = request.POST.getlist('perfilesOrganizacion')

            if not all([nombre_organizacion, fecha_integracion, comuna_id, direccion]):
                messages.error(request, 'Todos los campos marcados con * son obligatorios.')
                return redirect('dashboarda:crear_juntavecinos')

            # Validar que la comuna exista
            try:
                comuna = Comuna.objects.get(id_comuna=comuna_id)
            except Comuna.DoesNotExist:
                messages.error(request, 'La comuna seleccionada no existe.')
                return redirect('dashboarda:crear_juntavecinos')

            # Validar que no exista otra junta de vecinos con el mismo nombre en la misma comuna
            if JuntaVecinos.objects.filter(
                nombre_organizacion=nombre_organizacion, 
                id_comuna=comuna
            ).exists():
                messages.error(request, 'Ya existe una junta de vecinos con ese nombre en la comuna seleccionada.')
                return redirect('dashboarda:crear_juntavecinos')

            estado_inicial = EstadoJuntaVecinos.objects.get(id_estado=1) 

            # Crear la junta de vecinos
            junta_vecinos = JuntaVecinos.objects.create(
                nombre_organizacion=nombre_organizacion,
                fecha_integracion=fecha_integracion,
                id_comuna=comuna,
                direccion=direccion,
                id_estado=estado_inicial
            )

            if perfiles_seleccionados:
                perfiles = Perfiles.objects.filter(rut__in=perfiles_seleccionados)
                junta_vecinos.perfiles.set(perfiles)

            messages.success(request, 'Junta de vecinos creada exitosamente.')
            return redirect('dashboarda:juntavecinos')  

        except ValueError as e:
            messages.error(request, f'Error de validación: {str(e)}')
            return redirect('dashboarda:crear_junta_vecinos')
        except Exception as e:
            messages.error(request, f'Error al crear la junta de vecinos: {str(e)}')
            return redirect('dashboarda:crear_junta_vecinos')



@method_decorator([login_required, role_required(1)], name='dispatch')
class EditarJuntaVecinosView(View):
    def get(self, request, id_juntavecino, *args, **kwargs):
        junta_vecinos = get_object_or_404(JuntaVecinos, id_juntavecino=id_juntavecino)
        regiones = Region.objects.all()
        comunas = Comuna.objects.filter(id_region=junta_vecinos.id_comuna.id_region)
        estados = EstadoJuntaVecinos.objects.all()
        perfiles = Perfiles.objects.all()
        perfiles_asociados = junta_vecinos.perfiles.all()
        
        context = {
            'junta_vecinos': junta_vecinos,
            'regiones': regiones,
            'comunas': comunas,
            'estados': estados,
            'perfiles': perfiles,
            'perfiles_asociados': perfiles_asociados,
        }
        return render(request, 'dashboarda/editarjuntavecino.html', context)
    
    def post(self, request, id_juntavecino, *args, **kwargs):
        junta_vecinos = get_object_or_404(JuntaVecinos, id=id_juntavecino)
        
        try:
            nombre_organizacion = request.POST.get('nombreOrganizacion')
            fecha_integracion = request.POST.get('fechaIntegracion')
            comuna_id = request.POST.get('comuna')
            direccion = request.POST.get('direccionOrganizacion')
            perfiles_seleccionados = request.POST.getlist('perfilesOrganizacion')

            if not all([nombre_organizacion, fecha_integracion, comuna_id, direccion]):
                messages.error(request, 'Todos los campos marcados con * son obligatorios.')
                return redirect('dashboarda:editar_juntavecinos', id_juntavecino=id_juntavecino)

            # Validar que la comuna exista
            try:
                comuna = Comuna.objects.get(id_comuna=comuna_id)
            except Comuna.DoesNotExist:
                messages.error(request, 'La comuna seleccionada no existe.')
                return redirect('dashboarda:editar_juntavecinos', id_juntavecino=id_juntavecino)

            # Validar que no exista otra junta de vecinos con el mismo nombre en la misma comuna
            if JuntaVecinos.objects.filter(
                nombre_organizacion=nombre_organizacion,
                id_comuna=comuna
            ).exclude(id=id_juntavecino).exists():
                messages.error(request, 'Ya existe una junta de vecinos con ese nombre en la comuna seleccionada.')
                return redirect('dashboarda:editar_juntavecinos', id_juntavecino=id_juntavecino)

            # Actualizar datos de la junta de vecinos
            junta_vecinos.nombre_organizacion = nombre_organizacion
            junta_vecinos.fecha_integracion = fecha_integracion
            junta_vecinos.id_comuna = comuna
            junta_vecinos.direccion = direccion
            junta_vecinos.save()

            # Actualizar perfiles asociados
            if perfiles_seleccionados:
                perfiles = Perfiles.objects.filter(rut__in=perfiles_seleccionados)
                junta_vecinos.perfiles.set(perfiles)

            messages.success(request, 'Junta de vecinos actualizada exitosamente.')
            return redirect('dashboarda:juntavecinos')

        except ValueError as e:
            messages.error(request, f'Error de validación: {str(e)}')
            return redirect('dashboarda:editar_juntavecinos', id_juntavecino=id_juntavecino)
        except Exception as e:
            messages.error(request, f'Error al actualizar la junta de vecinos: {str(e)}')
            return redirect('dashboarda:editar_juntavecinos', id_juntavecino=id_juntavecino)
        
        
        
@method_decorator([login_required, role_required(1)], name='dispatch')
class JuntaVecinosView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        juntas = JuntaVecinos.objects.select_related('id_comuna', 'id_comuna__id_region').all()
        
        context = {
            'user': user,
            'juntas': juntas,
        }
        return render(request, 'dashboarda/listajuntavecinos.html', context)
    

@method_decorator([login_required, role_required(1)], name='dispatch')
class PerfilesJuntaVecino(View):
    def get(self, request, id_juntavecino, *args, **kwargs):
        junta = get_object_or_404(JuntaVecinos, id_juntavecino=id_juntavecino)

        perfiles = junta.perfiles.filter(id_rol=2)
        
        perfiles_habilitados = perfiles.filter(id_estadoperfil=1).count()
        perfiles_inhabilitados = perfiles.filter(id_estadoperfil=2).count()
        
        return render(request, 'dashboarda/perfilesjuntavecino.html', {
            'junta': junta,
            'perfiles': perfiles,
            'perfiles_habilitados': perfiles_habilitados,
            'perfiles_inhabilitados': perfiles_inhabilitados
        })
        
        
@method_decorator([login_required, role_required(1)], name='dispatch')
class VecinosJuntaVecino(View):
    def get(self, request, id_juntavecino, *args, **kwargs):
        junta = get_object_or_404(JuntaVecinos, id_juntavecino=id_juntavecino)

        vecinos = junta.perfiles.filter(id_rol=3)
        
        vecinos_habilitados = vecinos.filter(id_estadoperfil=1).count()
        vecinos_inhabilitados = vecinos.filter(id_estadoperfil=2).count()
        
        return render(request, 'dashboarda/vecinosjuntavecino.html', {
            'junta': junta,
            'vecinos': vecinos,
            'vecinos_habilitados': vecinos_habilitados,
            'vecinos_inhabilitados': vecinos_inhabilitados
        })

        
        
@csrf_exempt
def filter_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filter_type = data.get('filter_type')
            filter_value = data.get('filter_value')
            
            # Inicializar valores
            total_juntas = 0
            habilitadas_juntas = 0
            inhabilitadas_juntas = 0
            
            # Obtener la fecha de filtro para 'fecha_integracion'
            if filter_value == 'today':
                date_filter = datetime.now().date()
                date_query_integracion = Q(fecha_integracion=date_filter)
                date_query_termino = Q(fecha_termino=date_filter)
            elif filter_value == 'week':
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                date_query_integracion = Q(fecha_integracion__gte=week_start)
                date_query_termino = Q(fecha_termino__gte=week_start)
            elif filter_value == 'month':
                month_start = datetime.now().replace(day=1)
                date_query_integracion = Q(fecha_integracion__gte=month_start)
                date_query_termino = Q(fecha_termino__gte=month_start)
            elif filter_value == 'year':
                year_start = datetime.now().replace(month=1, day=1)
                date_query_integracion = Q(fecha_integracion__gte=year_start)
                date_query_termino = Q(fecha_termino__gte=year_start)
            else:
                date_query_integracion = Q()
                date_query_termino = Q()
            
            # Aplicar filtros según el tipo
            if filter_type == 'total':
                total_juntas = JuntaVecinos.objects.filter(date_query_integracion).count()
            elif filter_type == 'habilitadas':
                habilitadas_juntas = JuntaVecinos.objects.filter(date_query_integracion, id_estado=1).count()
            elif filter_type == 'inhabilitadas':
                # Filtrar por `fecha_termino` para inhabilitadas
                inhabilitadas_juntas = JuntaVecinos.objects.filter(date_query_termino, id_estado=2).count()

            return JsonResponse({
                'total_juntas': total_juntas,
                'habilitadas_juntas': habilitadas_juntas,
                'inhabilitadas_juntas': inhabilitadas_juntas
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def reset_data(request):
    if request.method == 'POST':
        try:
            total_juntas = JuntaVecinos.objects.count()
            habilitadas_juntas = JuntaVecinos.objects.filter(id_estado=1).count()
            inhabilitadas_juntas = JuntaVecinos.objects.filter(id_estado=2).count()

            return JsonResponse({
                'total_juntas': total_juntas,
                'habilitadas_juntas': habilitadas_juntas,
                'inhabilitadas_juntas': inhabilitadas_juntas
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


    
@method_decorator([login_required, role_required(1)], name='dispatch')
class DashboardAdminView(TemplateView):
    template_name = 'dashboarda/dashboardadmin.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        total_juntas = JuntaVecinos.objects.count()
        habilitadas_juntas = JuntaVecinos.objects.filter(id_estado=1).count()
        inhabilitadas_juntas = JuntaVecinos.objects.filter(id_estado=2).count()
        
        context.update({
            'user': user,
            'total_juntas': total_juntas,
            'habilitadas_juntas': habilitadas_juntas,
            'inhabilitadas_juntas': inhabilitadas_juntas
        })
        return context
    
@method_decorator([login_required, role_required(1)], name='dispatch')
class JuntaVecinosRegiones(TemplateView):
    template_name = 'dashboarda/regionesjuntas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        comunas = Comuna.objects.all()
        juntas = JuntaVecinos.objects.select_related('id_comuna', 'id_comuna__id_region').all()
        
        context.update({
            'user': user,
            'comunas': comunas,
            'juntas': juntas
        })
        return context