# Generated by Django 4.2.3 on 2023-11-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyApp', '0006_comment_community_communitystudent_course_file_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='Aemail',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Semail',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Sgender',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='Sgrade',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='Smajor',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
