# Generated by Django 4.2.3 on 2023-11-11 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyApp', '0011_alter_image_iname'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Plikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='CommentLikes',
            field=models.IntegerField(default=0),
        ),
    ]
