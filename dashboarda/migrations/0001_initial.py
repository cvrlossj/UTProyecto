# Generated by Django 5.1.2 on 2024-11-13 02:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_estadoactividad_estadocertificado_estadonoticia_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JuntaVecinos',
            fields=[
                ('id_juntavecino', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre_organizacion', models.CharField(max_length=100)),
                ('fecha_integracion', models.DateField()),
                ('fecha_termino', models.DateField(blank=True)),
                ('direccion', models.CharField(max_length=100)),
                ('id_comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.comuna')),
                ('perfiles', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
