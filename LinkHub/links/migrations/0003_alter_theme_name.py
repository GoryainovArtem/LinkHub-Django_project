# Generated by Django 4.1.7 on 2023-04-01 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_remove_project_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='name',
            field=models.SlugField(unique=True, verbose_name='Название'),
        ),
    ]
