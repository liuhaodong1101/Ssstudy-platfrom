# Generated by Django 4.2.3 on 2023-11-27 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudyApp', '0015_appconfig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='Sgender',
        ),
    ]