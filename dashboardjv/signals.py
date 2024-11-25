from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import EstadoNoticia, EstadoActividad, EstadoCertificado, EstadoPostulacion

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name == 'dashboardjv':
            EstadoNoticia.objects.get_or_create(id_estadonoticia=1, descripcion='habilitada')
            EstadoNoticia.objects.get_or_create(id_estadonoticia=2, descripcion='inhabilitada')
            
            EstadoActividad.objects.get_or_create(id_estadoactividad=1, descripcion='habilitada')
            EstadoActividad.objects.get_or_create(id_estadoactividad=2, descripcion='inhabilitada')
            
            EstadoCertificado.objects.get_or_create(id_estadocertificado=1, descripcion='pendiente')
            EstadoCertificado.objects.get_or_create(id_estadocertificado=2, descripcion='emitido')
            EstadoCertificado.objects.get_or_create(id_estadocertificado=3, descripcion='aprobar')
            EstadoCertificado.objects.get_or_create(id_estadocertificado=4, descripcion='rechazar')
            
            EstadoPostulacion.objects.get_or_create(id_estadopostulacion=1, descripcion='pendiente')
            EstadoPostulacion.objects.get_or_create(id_estadopostulacion=2, descripcion='aprobado')
            EstadoPostulacion.objects.get_or_create(id_estadopostulacion=3, descripcion='rechazado')