from django.contrib import admin
from .models import Noticias, EstadoPostulacion, EstadoCertificado, EstadoNoticia, EstadoActividad, Actividad, PostulacionProyectos



@admin.register(Noticias)
class NoticiasAdmin(admin.ModelAdmin):
   list_display = ('id_noticia', 'nombre','fecha_inicio', 'fecha_termino')
   search_fields = ('nombre',)


@admin.register(EstadoPostulacion)
class EstadoPostulacionAdmin(admin.ModelAdmin):
   list_display = ('id_estadopostulacion', 'descripcion')
   search_fields = ('descripcion',)

@admin.register(EstadoCertificado)
class EstadoCertificadoAdmin(admin.ModelAdmin):
   list_display = ('id_estadocertificado', 'descripcion')
   search_fields = ('descripcion',)
   
@admin.register(EstadoNoticia)
class EstadoNoticiaAdmin(admin.ModelAdmin):
   list_display = ('id_estadonoticia', 'descripcion')
   search_fields = ('descripcion',)
   
@admin.register(EstadoActividad)
class EstadoActividadAdmin(admin.ModelAdmin):
   list_display = ('id_estadoactividad', 'descripcion')
   search_fields = ('descripcion',)
   
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
   list_display = ('id_actividad', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_termino', 'horario_inicio', 'horario_termino', 'id_estadoactividad')
   search_fields = ('nombre', 'descripcion')
