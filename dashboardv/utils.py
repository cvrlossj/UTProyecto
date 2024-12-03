from django.http import JsonResponse
from django.views import View
from dashboarda.models import JuntaVecinos
from accounts.models import Perfiles

class BuscarMiembroPerfil(View):
    def get(self, request, *args, **kwargs):
        rut = request.GET.get('rut', '').strip()
        user = request.user
        
        try:
            junta = JuntaVecinos.objects.filter(perfiles=user).first()
            if not junta:
                return JsonResponse({'success': False, 'error': 'No estás asociado a una junta de vecinos'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        try:
            titular = Perfiles.objects.get(
                rut__startswith=rut,
                id_rol=3,  
                id_estadoperfil=1 
            )
            
            if not titular.juntavecinos_set.filter(id_juntavecino=junta.id_juntavecino).exists():
                return JsonResponse({'success': False, 'error': 'El titular no pertenece a esta junta de vecinos'})

        except Perfiles.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El RUT no pertenece a un titular válido'})

        if titular.familia:
            miembros = Perfiles.objects.filter(
                familia=titular.familia,
                id_rol=3,
                id_estadoperfil=1
            ).filter(
                juntavecinos__id_juntavecino=junta.id_juntavecino
            ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')
        else:
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


# API para buscar miembros de la familia de un titular a través de un SELECT
class ObtenerMiembrosFamilia(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Validar que el usuario está asociado a una junta de vecinos
        try:
            junta = JuntaVecinos.objects.filter(perfiles=user).first()
            if not junta:
                return JsonResponse({'success': False, 'error': 'No estás asociado a una junta de vecinos'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        # Obtener la familia del titular
        try:
            # Obtener el perfil del usuario y acceder a la familia
            perfil = Perfiles.objects.get(rut=user.rut)
            familia = perfil.familia
        except Perfiles.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No se encontró el perfil del titular'})

        # Obtener miembros de la familia (si tiene familia)
        if familia:
            miembros = Perfiles.objects.filter(
                familia=familia,
                id_rol=3,  # Rol de vecino
                id_estadoperfil=1  # Perfil activo
            ).filter(
                juntavecinos__id_juntavecino=junta.id_juntavecino
            ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')
        else:
            # Si no hay familia, solo devolver el titular
            miembros = Perfiles.objects.filter(
                rut=perfil.rut,
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
