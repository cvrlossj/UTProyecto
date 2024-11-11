from django.db import models
from accounts.models import Comuna, Perfiles

class JuntaVecinos(models.Model):
 id_juntavecino = models.AutoField(unique=True, primary_key=True)
 nombre_organizacion = models.CharField(max_length=100)
 id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
 fecha_integracion = models.DateField()
 fecha_termino = models.DateField()
 direccion = models.CharField(max_length=100)
 perfiles = models.ManyToManyField(Perfiles)