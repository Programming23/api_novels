# Generated by Django 3.2.8 on 2022-10-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_image_anime_novel_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='link',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
