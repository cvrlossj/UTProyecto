# Generated by Django 5.1.2 on 2024-11-06 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comuna',
            name='id_comuna',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='estado',
            name='id_estado',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='parentesco',
            name='id_parentesco',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='correo_electronico',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='direccion',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='fecha_incorporacion',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='fecha_nacimiento',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='fecha_termino',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_comuna',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.comuna'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_estado',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.estado'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_parentesco',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.parentesco'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_region',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.region'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_rol',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.roles'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='id_sexo',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sexo'),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='numero_contacto',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='perfiles',
            name='rut',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='id_region',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='id_rol',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sexo',
            name='id_sexo',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
