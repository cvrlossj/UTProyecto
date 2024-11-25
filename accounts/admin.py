from django.contrib import admin
from .models import EstadoPerfil, Region, Comuna, Roles, Sexo, Parentesco, Perfiles, Familia

@admin.register(EstadoPerfil)
class EstadoPerfilAdmin(admin.ModelAdmin):
   list_display = ('id_estadoperfil', 'descripcion')
   search_fields = ('descripcion',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
   list_display = ('id_region', 'nombre_region')
   search_fields = ('nombre_region',)
   
@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
      list_display = ('id_comuna', 'nombre_comuna', 'nombre_region')
      search_fields = ('nombre_comuna', 'id_region__nombre_region')

      def nombre_region(self, obj):
         return obj.id_region.nombre_region

      nombre_region.short_description = 'Nombre de Región'
   
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
   list_display = ('id_rol', 'descripcion')
   search_fields = ('descripcion',)
   

@admin.register(Sexo)
class SexoAdmin(admin.ModelAdmin):
   list_display = ('id_sexo', 'descripcion')
   search_fields = ('descripcion',)


@admin.register(Parentesco)
class ParentescoAdmin(admin.ModelAdmin):
   list_display = ('id_parentesco', 'descripcion')
   search_fields = ('descripcion',)

@admin.register(Perfiles)
class PerfilesAdmin(admin.ModelAdmin):
   list_display = ('rut', 'nombre', 'apellido', 'numero_contacto', 'correo_electronico', 'id_estadoperfil')
   search_fields = ('nombre', 'apellido', 'rut')
   

@admin.register(Familia)
class FamiliasAdmin(admin.ModelAdmin):
   list_display = ('id_familia', 'nombre')
   search_fields = ('nombre',)