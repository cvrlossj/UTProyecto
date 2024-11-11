from django.contrib import admin
from .models import JuntaVecinos
# Register your models here.

@admin.register(JuntaVecinos)
class JuntaVecinoAdmin(admin.ModelAdmin):
   list_display = ('id_juntavecino', 'nombre_organizacion', 'fecha_integracion', 'direccion', 'id_comuna')
   search_fields = ('nombre_organizacion',)
