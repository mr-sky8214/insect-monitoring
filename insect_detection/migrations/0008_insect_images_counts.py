# Generated by Django 2.2 on 2021-11-25 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insect_detection', '0007_remove_insect_images_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='insect_images',
            name='counts',
            field=models.TextField(blank=True, default=''),
        ),
    ]
