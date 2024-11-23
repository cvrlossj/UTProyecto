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
