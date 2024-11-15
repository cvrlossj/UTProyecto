# Generated by Django 5.1.2 on 2024-11-09 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboardjv', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadoactividad',
            name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='estadoactividad',
            name='fecha_termino',
        ),
        migrations.RemoveField(
            model_name='estadoactividad',
            name='horario_inicio',
        ),
        migrations.RemoveField(
            model_name='estadoactividad',
            name='horario_termino',
        ),
        migrations.RemoveField(
            model_name='estadoactividad',
            name='id_actividad',
        ),
        migrations.RemoveField(
            model_name='estadoactividad',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='estadoactividad',
            name='descripcion',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='estadoactividad',
            name='id_estadoactividad',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id_actividad', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=80)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('horario_inicio', models.TimeField()),
                ('horario_termino', models.TimeField()),
                ('id_estadoactividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboardjv.estadonoticia')),
            ],
        ),
    ]
