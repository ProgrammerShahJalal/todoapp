# Generated by Django 4.2.4 on 2023-11-04 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0009_taskmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='todoapp/static/todoapp'),
        ),
    ]
