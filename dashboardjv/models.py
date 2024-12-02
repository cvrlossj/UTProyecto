from django.db import models
from accounts.models import Perfiles
from dashboarda.models import JuntaVecinos


class EstadoPostulacion(models.Model):
  id_estadopostulacion = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=20)

class EstadoCertificado(models.Model):
  id_estadocertificado = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)

class EstadoNoticia(models.Model):
  id_estadonoticia = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
class EstadoActividad(models.Model):
  id_estadoactividad = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)

class Actividad(models.Model):
  id_actividad = models.AutoField(unique=True, primary_key=True)
  nombre = models.CharField(max_length=80)
  descripcion = models.TextField()
  fecha_inicio = models.DateField()
  horario_inicio = models.TimeField()
  horario_termino = models.TimeField()
  periodo_inicio = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')], default='AM')
  periodo_termino = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')], default='AM')
  cupos = models.IntegerField()
  id_estadoactividad = models.ForeignKey(EstadoActividad, on_delete=models.CASCADE)
  id_juntavecinos = models.ForeignKey(JuntaVecinos, on_delete=models.CASCADE)

class InscripcionActividad(models.Model):
  id_inscripcion = models.AutoField(unique=True, primary_key=True)
  id_perfil = models.ForeignKey(Perfiles, on_delete=models.CASCADE)
  id_actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
  fecha_inscripcion = models.DateField(auto_now_add=True)

  class Meta:
    unique_together = ['id_perfil', 'id_actividad'] # evitamos inscripciones duplicadas
  
  def __str__(self):
    return f"Inscripción de {self.id_perfil} en la actividad {self.id_actividad}"

  def save(self, *args, **kwargs):
        # Verificar si hay cupos disponibles antes de guardar
        if self.id_actividad.cupos <= InscripcionActividad.objects.filter(id_actividad=self.id_actividad).count():
            raise ValueError("No hay cupos disponibles para esta actividad.")
        super().save(*args, **kwargs)

class PostulacionProyectos(models.Model):
  id_proyecto = models.AutoField(unique=True, primary_key=True)
  titulo = models.CharField(max_length=150)
  descripcion = models.TextField()
  objetivos = models.TextField()
  presupuesto = models.DecimalField(max_digits=15, decimal_places=2)
  id_juntavecinos = models.ForeignKey(JuntaVecinos, on_delete=models.CASCADE)
  rut_postulante = models.ForeignKey(Perfiles, on_delete=models.CASCADE)
  id_estadopostulacion = models.ForeignKey(EstadoPostulacion, on_delete=models.CASCADE)
  
class CertificadosResi(models.Model):
  id_certificado = models.AutoField(unique=True, primary_key=True)
  nombre_postulante = models.CharField(max_length=120)
  direccion_postulante = models.CharField(max_length=120)
  fecha_emision = models.DateField(null=True, blank=True)
  nota_estado = models.CharField(max_length=120, null=True, blank=True)
  id_juntavecinos = models.ForeignKey(JuntaVecinos, on_delete=models.CASCADE)
  rut_postulante = models.ForeignKey(Perfiles, on_delete=models.CASCADE)
  id_estadocertificado = models.ForeignKey(EstadoCertificado, on_delete=models.CASCADE)

class Noticias(models.Model):
  id_noticia = models.AutoField(unique=True, primary_key=True)
  nombre = models.CharField(max_length=80)
  descripcion = models.TextField()
  fecha_inicio = models.DateField()
  fecha_termino = models.DateField(null=True, blank=True)
  id_estadonoticia = models.ForeignKey(EstadoNoticia, on_delete=models.CASCADE)
  id_juntavecinos = models.ForeignKey(JuntaVecinos, on_delete=models.CASCADE)
  
  def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio} - {self.fecha_termino})"