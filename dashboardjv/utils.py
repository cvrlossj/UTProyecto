from django.http import JsonResponse
from django.views import View
from dashboarda.models import JuntaVecinos
from accounts.models import Perfiles

class BuscarPerfil(View):
    def get(self, request, *args, **kwargs):
        rut = request.GET.get('rut', '')
        user = request.user
        
        try:
            junta = JuntaVecinos.objects.get(perfiles=user)
        except JuntaVecinos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No estás asociado a una junta de vecinos'})
        
        if rut:
            perfiles = Perfiles.objects.filter(
                rut__startswith=rut,
                id_estadoperfil=1,
                id_rol=3, 
                juntavecinos=junta
            ).values('rut', 'dv', 'nombre', 'apellido', 'correo_electronico', 'direccion')
            
            if perfiles.exists():
                return JsonResponse({'success': True, 'data': list(perfiles)})
            else:
                return JsonResponse({'success': False, 'error': 'No se encontró ningún perfil'})
        
        return JsonResponse({'success': False, 'error': 'Rut no proporcionado'})