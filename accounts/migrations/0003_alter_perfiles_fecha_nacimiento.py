# Generated by Django 5.1.2 on 2024-11-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_comuna_id_comuna_alter_estado_id_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfiles',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
