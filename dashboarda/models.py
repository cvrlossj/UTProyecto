from django.db import models
from accounts.models import Comuna, Perfiles
from .utils import obtener_coordenadas

class EstadoJuntaVecinos(models.Model):
      id_estado = models.AutoField(unique=True, primary_key=True)
      nombre_estado = models.CharField(max_length=100)

      def __str__(self):
            return f"{self.id_estado} - {self.nombre_estado}"

class JuntaVecinos(models.Model):
      id_juntavecino = models.AutoField(unique=True, primary_key=True)
      nombre_organizacion = models.CharField(max_length=100)
      id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
      fecha_integracion = models.DateField()
      fecha_termino = models.DateField(blank=True, null=True)
      direccion = models.CharField(max_length=100)
      id_estado = models.ForeignKey(EstadoJuntaVecinos, on_delete=models.CASCADE)
      perfiles = models.ManyToManyField(Perfiles, blank=True)
      
      # Campos para las coordenadas
      latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
      longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

      def save(self, *args, **kwargs):
            # Si no hay coordenadas guardadas, intenta obtenerlas automáticamente
            if not self.latitud or not self.longitud:
                  comuna_nombre = self.id_comuna.nombre_comuna
                  region_nombre = self.id_comuna.id_region.nombre_region
                  direccion = self.direccion
                  
                  # Llamar a la función con dirección, comuna y región
                  lat, lon = obtener_coordenadas(direccion, comuna_nombre, region_nombre)
                  
                  print(f"Coordenadas obtenidas: lat={lat}, lon={lon}")  # <-- Depuración
                  
                  if lat and lon:
                        self.latitud = lat
                        self.longitud = lon
            
            super().save(*args, **kwargs)


      def __str__(self):
            return f"{self.nombre_organizacion} - {self.id_comuna}"