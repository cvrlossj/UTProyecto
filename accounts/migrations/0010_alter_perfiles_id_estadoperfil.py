# Generated by Django 5.1.2 on 2024-11-20 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_estadoactividad_estadocertificado_estadonoticia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiles',
            name='id_estadoperfil',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.estadoperfil'),
        ),
    ]
