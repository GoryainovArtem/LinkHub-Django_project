# Generated by Django 4.1.7 on 2023-03-30 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название', max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Добавьте описание', null=True, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name='дата последнего редактирования')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название', max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Добавьте описание', null=True, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name='дата последнего редактирования')),
                ('is_private', models.BooleanField(choices=[(True, 'Private'), (False, 'Public')], default=False, help_text='Укажите, кому будет доступен этот проект: public - доступен только создателю и редакторам; private - доступен для всех пользователей', verbose_name='Тип проекта')),
                ('is_group_project', models.BooleanField(choices=[(True, 'Группа'), (False, 'Только я')], default=False, verbose_name='Кто может работать с проектом')),
                ('editor', models.ManyToManyField(blank=True, null=True, related_name='projects_edit', to=settings.AUTH_USER_MODEL, verbose_name='Редакторы')),
                ('main_admin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_projects', to=settings.AUTH_USER_MODEL, verbose_name='создатель')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='links.project')),
            ],
            options={
                'verbose_name': 'Звезда',
                'verbose_name_plural': 'Звезды',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='theme',
            field=models.ManyToManyField(blank=True, help_text='Выберите тематику проекта', null=True, related_name='projects', to='links.theme', verbose_name='Тематика'),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название', max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Добавьте описание', null=True, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name='дата последнего редактирования')),
                ('url', models.URLField(verbose_name='ссылка')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='links.head')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
        migrations.AddField(
            model_name='head',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heads', to='links.project'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='links.link')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
            },
        ),
    ]