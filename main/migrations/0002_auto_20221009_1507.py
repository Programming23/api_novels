# Generated by Django 3.2.8 on 2022-10-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='novel',
            old_name='anime_type',
            new_name='novel_type',
        ),
        migrations.AlterField(
            model_name='novel',
            name='image_anime',
            field=models.ImageField(default='', upload_to='photos/novels'),
        ),
    ]
