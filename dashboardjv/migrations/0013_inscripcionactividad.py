# Generated by Django 5.1.2 on 2024-12-02 03:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardjv', '0012_remove_actividad_fecha_termino_actividad_cupos'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InscripcionActividad',
            fields=[
                ('id_inscripcion', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboardjv.actividad')),
                ('id_perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_perfil', 'id_actividad')},
            },
        ),
    ]
