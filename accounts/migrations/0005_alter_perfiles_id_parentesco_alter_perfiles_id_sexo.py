# Generated by Django 5.1.2 on 2024-11-06 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_perfiles_fecha_incorporacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiles',
            name='id_parentesco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.parentesco'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_sexo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sexo'),
        ),
    ]