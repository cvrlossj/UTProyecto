# Generated by Django 5.1.2 on 2024-11-23 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboarda', '0005_juntavecinos_latitud_juntavecinos_longitud'),
        ('dashboardjv', '0003_alter_certificadosresi_id_juntavecino_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticias',
            name='id_juntavecinos',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='dashboarda.juntavecinos'),
            preserve_default=False,
        ),
    ]
