from django.db import models
from accounts.models import Comuna, Perfiles

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