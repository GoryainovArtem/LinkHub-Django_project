# Generated by Django 4.1.7 on 2023-04-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_alter_head_options_alter_head_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='number',
            field=models.IntegerField(blank=True, help_text='Укажите номер источника. Параметр необязателен и может быть выставлен автоматически', null=True, verbose_name='номер источника'),
        ),
    ]
