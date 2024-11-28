from django.http import JsonResponse
from django.views import View
from dashboarda.models import JuntaVecinos
from accounts.models import Perfiles

class BuscarMiembroPerfil(View):
    def get(self, request, *args, **kwargs):
        rut = request.GET.get('rut', '').strip()
        user = request.user
        
        # Validar que el usuario está asociado a una junta de vecinos
        try:
            # Cambiamos la forma de obtener la junta de vecinos
            junta = JuntaVecinos.objects.filter(perfiles=user).first()
            if not junta:
                return JsonResponse({'success': False, 'error': 'No estás asociado a una junta de vecinos'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        try:
            # Buscar el titular
            titular = Perfiles.objects.get(
                rut__startswith=rut,
                id_rol=3,  # Rol de vecino
                id_estadoperfil=1  # Perfil activo
            )
            
            # Verificar que el titular pertenece a la junta de vecinos
            if not titular.juntavecinos_set.filter(id_juntavecino=junta.id_juntavecino).exists():
                return JsonResponse({'success': False, 'error': 'El titular no pertenece a esta junta de vecinos'})

        except Perfiles.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El RUT no pertenece a un titular válido'})

        # Obtener miembros de la familia
        if titular.familia:
            miembros = Perfiles.objects.filter(
                familia=titular.familia,
                id_rol=3,
                id_estadoperfil=1
            ).filter(
                juntavecinos__id_juntavecino=junta.id_juntavecino
            ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')
        else:
            # Si el titular no tiene familia, devolver solo al titular
            miembros = Perfiles.objects.filter(
                rut=titular.rut,
                id_rol=3,
                id_estadoperfil=1
            ).filter(
                juntavecinos__id_juntavecino=junta.id_juntavecino
            ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')

        miembros_list = list(miembros)
        
        if not miembros_list:
            return JsonResponse({
                'success': False, 
                'error': 'No se encontraron miembros de la familia para este titular en esta junta de vecinos'
            })

        return JsonResponse({'success': True, 'miembros': miembros_list})




# Version 2

# class BuscarMiembroPerfil(View):
#     def get(self, request, *args, **kwargs):
#         rut = request.GET.get('rut', '').strip()
#         user = request.user
        
#         # Validar que el usuario está asociado a una junta de vecinos
#         try:
#             junta = JuntaVecinos.objects.filter(perfiles=user).first()
#             if not junta:
#                 return JsonResponse({'success': False, 'error': 'No estás asociado a una junta de vecinos'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#         try:
#             titulares = Perfiles.objects.filter(
#                 rut__icontains=rut,
#                 id_rol=3,
#                 id_estadoperfil=1
#             ).filter(
#                 juntavecinos__id_juntavecino=junta.id_juntavecino
#             ).values(
#                 'rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion', 'familia'
#             ).distinct()


#             if not titulares.exists():
#                 return JsonResponse({'success': False, 'error': 'No se encontraron titulares válidos'})

#             # Construir la lista de miembros de la familia
#             miembros_list = []
#             for titular in titulares:
#                 if titular['familia']:
#                     miembros = Perfiles.objects.filter(
#                         familia=titular['familia'],
#                         id_rol=3,
#                         id_estadoperfil=1
#                     ).filter(
#                         juntavecinos__id_juntavecino=junta.id_juntavecino
#                     ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')
#                     miembros_list.extend(list(miembros))
#                 else:
#                     miembros_list.append(titular)

#             if not miembros_list:
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'No se encontraron miembros de la familia para estos titulares'
#                 })

#             return JsonResponse({'success': True, 'miembros': miembros_list})

#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
