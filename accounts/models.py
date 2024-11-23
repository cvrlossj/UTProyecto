from django.contrib.auth.base_user import BaseUserManager 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class PerfilesManager(BaseUserManager):
    def create_user(
        self, rut, 
        correo_electronico, 
        password= str, 
        **extra_fields: dict[str, str | bool],
      ) -> "Perfiles":
        if not rut:
            raise ValueError("The RUT must be set")
        if not correo_electronico:
            raise ValueError("The Email must be set")
        correo_electronico = self.normalize_email(correo_electronico)
        user: Perfiles = self.model(rut=rut, correo_electronico=correo_electronico, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
          self, 
          rut, 
          correo_electronico, 
          password=str, 
          **extra_fields: dict[str, str | bool],
      ) -> "Perfiles":
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(rut, correo_electronico, password, **extra_fields)

class EstadoPerfil(models.Model):
  id_estadoperfil = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
  def __str__(self):
      return f"{self.id_estadoperfil} - {self.descripcion}"
    
class EstadoNoticia(models.Model):
  id_estadonoticia = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
  def __str__(self):
      return f"{self.id_estadonoticia} - {self.descripcion}"
    
class EstadoActividad(models.Model):
  id_estadoactividad = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
  def __str__(self):
      return f"{self.id_estadoactividad} - {self.descripcion}"
    
class EstadoCertificado(models.Model):
  id_estadocertificado = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
  def __str__(self):
      return f"{self.id_estadocertificado} - {self.descripcion}"

class EstadoPostulacion(models.Model):
  id_estadopostulacion = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=30)
  
  def __str__(self):
      return f"{self.id_estadopostulacion} - {self.descripcion}"

class Region(models.Model):
  id_region = models.AutoField(unique=True, primary_key=True)
  nombre_region = models.CharField(max_length=80)
  
  def __str__(self):
      return f"{self.nombre_region}"

class Comuna(models.Model):
  id_comuna = models.AutoField(unique=True, primary_key=True)
  nombre_comuna = models.CharField(unique=True, max_length=80)
  id_region = models.ForeignKey(Region, on_delete=models.CASCADE)

  def __str__(self):
      return f"{self.nombre_comuna}"


class Roles(models.Model):
  id_rol = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=50)
  
  def __str__(self):
      return f"{self.id_rol} - {self.descripcion}"


class Sexo(models.Model):
  id_sexo = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=10)
  
  def __str__(self):
      return f"{self.descripcion}"


class Parentesco(models.Model):
  id_parentesco = models.AutoField(unique=True, primary_key=True)
  descripcion = models.CharField(max_length=50)

  def __str__(self):
      return f"{self.id_parentesco} - {self.descripcion}"

class Perfiles(AbstractUser):
  username = None
  first_name = None
  last_name = None
  email = None
  rut = models.IntegerField(unique=True, primary_key=True)
  dv = models.CharField(max_length=1)
  nombre = models.CharField(max_length=60)
  apellido = models.CharField(max_length=60)
  fecha_nacimiento = models.DateField(null=True, blank=True)
  id_sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True, blank=True)
  id_parentesco = models.ForeignKey(Parentesco, on_delete=models.CASCADE, null=True, blank=True)
  direccion = models.CharField(max_length=100, blank=True)
  numero_contacto = models.CharField(max_length=11)
  correo_electronico = models.CharField(max_length=80, blank=True)
  fecha_incorporacion = models.DateField(null=True, blank=True)
  fecha_termino = models.DateField(null=True, blank=True)
  id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
  id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True, blank=True)
  id_estadoperfil = models.ForeignKey(EstadoPerfil, on_delete=models.CASCADE, null=True, blank=True, default=1)
  

  USERNAME_FIELD = 'rut'
  REQUIRED_FIELDS = ['correo_electronico', 'nombre', 'apellido']

  objects = PerfilesManager()

  def __str__(self):
    return f"{self.rut} - {self.nombre} {self.apellido}"