# Generated by Django 5.1.2 on 2024-11-06 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_perfiles_first_name_remove_perfiles_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfiles',
            name='email',
        ),
    ]
