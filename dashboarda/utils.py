from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
import requests



def obtener_coordenadas(direccion, comuna, region):
    # Crear una query más detallada
    query = f"{direccion}, {comuna}, {region}, Chile"
    print(f"Buscando coordenadas para: {query}")
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'CL'
    }
    
    # Agregar un User-Agent para evitar el bloqueo
    headers = {
        'User-Agent': 'mi_app_juntas_vecinos/1.0 (carlossilvasilvadiaz@gmail.com)'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        
        # Depuración: Verificar la respuesta del servidor
        print("Respuesta de Nominatim:", response.json())
        
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data['lat']), float(data['lon'])
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a Nominatim: {e}")
    
    return None, None



def role_required(role_id):
    """
    Decorador para restringir vistas según el id_rol del usuario.
    
    :param role_id: ID del rol requerido para acceder a la vista.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.id_rol_id != role_id:
                # Redirige a la página de acceso denegado
                return redirect(reverse('dashboarda:acceso_denegado'))
            # Si pasa las validaciones, llama a la vista
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator