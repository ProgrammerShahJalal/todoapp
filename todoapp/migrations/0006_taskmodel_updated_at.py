# Generated by Django 4.2.4 on 2023-11-02 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_alter_taskmodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
