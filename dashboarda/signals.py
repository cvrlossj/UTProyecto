from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import EstadoJuntaVecinos

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
     if sender.name == 'dashboarda':
          EstadoJuntaVecinos.objects.get_or_create(id_estado=1, nombre_estado='habilitada')
          EstadoJuntaVecinos.objects.get_or_create(id_estado=2, nombre_estado='inhabilitada')