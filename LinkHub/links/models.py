from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max

from users.models import CustomUser


class BaseClass(models.Model):
    title = models.CharField('Название',
                             max_length=100,
                             help_text='Введите название')
    description = models.TextField('описание',
                                   help_text='Добавьте описание')
    created = models.DateTimeField('дата создания', auto_now_add=True)
    last_edit = models.DateTimeField('дата последнего редактирования', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Theme(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Project(BaseClass):
    ACCESS_TYPES = ((True, 'Private'), (False, 'Public'))
    theme = models.ManyToManyField(Theme,
                                   verbose_name='Тематика',
                                   related_name='projects',
                                   blank=True,
                                   help_text='Выберите тематику проекта. Для выбора нескольких значений зажмите Alt.')
    main_admin = models.ForeignKey(CustomUser,
                                   on_delete=models.DO_NOTHING,
                                   verbose_name='создатель',
                                   related_name='created_projects'
                                   )
    editor = models.ManyToManyField(CustomUser,
                                    verbose_name='Редакторы',
                                    related_name='projects_edit',
                                    blank=True
                                    )

    is_private = models.BooleanField('Тип проекта', default=False,
                                     choices=ACCESS_TYPES,
                                     help_text='Укажите, кому будет доступен этот проект: '
                                               'public - доступен только создателю и редакторам; '
                                               'private - доступен для всех пользователей')

    saved_users = models.ManyToManyField(CustomUser, related_name='saved_projects')
    liked_users = models.ManyToManyField(CustomUser, related_name='liked_users')

    source_amount = models.IntegerField(default=0)
    links_percentage = models.FloatField(default=0)
    image_percentage = models.FloatField(default=0)
    video_percentage = models.FloatField(default=0)
    document_percentage = models.FloatField(default=0)
    text_percentage = models.FloatField(default=0)
    stars_amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ('-created',)


class ProxyProjectOrderedDesc(Project):

    class Meta:
        proxy = True
        ordering = ('created',)


class ProxyProjectOrderedStars(Project):

    class Meta:
        proxy = True
        ordering = ('-stars_amount', '-created')


class Head(BaseClass):
    number = models.IntegerField('Номер раздела',
                                 blank=True, null=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='heads')

    class Meta:
        unique_together = ('project', 'number')
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.number:
            buf = self.project.heads.aggregate(max_number=Max('number'))
            if buf['max_number'] is None:
                value = 1
            else:
                value = buf['max_number'] + 1
            self.number = value
        super(Head, self).save()


class Link(BaseClass):
    description = models.TextField('описание',
                                   null=True,
                                   blank=True,
                                   help_text='Добавьте описание')
    number = models.IntegerField(
        'номер источника', blank=True,
        null=True,
        help_text='Укажите номер источника. '
                  'Параметр необязателен и может быть выставлен автоматически')
    url = models.URLField('Ссылка', blank=True, null=True)
    head = models.ForeignKey(Head,
                             on_delete=models.CASCADE,
                             related_name='links',
                             verbose_name='Раздел')

    document = models.FileField('Документ', blank=True, null=True,
                                upload_to='files/',
                                help_text='Выберите нужный документ')

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not (self.url or self.document or self.description):
            raise ValidationError('Хотя бы одно из полей: описание, ссылка, документ должно быть заполнено.')
        if self.number is None:
            buf = self.head.links.aggregate(max_number=Max('number'))
            if buf['max_number'] is None:
                value = 1
            else:
                value = buf['max_number'] + 1
            self.number = value
        super(Link, self).save()


class Comment(models.Model):
    DISPLAY_TEXT_LETTERS_AMOUNT = 15
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments')
    link = models.ForeignKey(Link,
                             on_delete=models.CASCADE,
                             related_name='comments')

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:self.DISPLAY_TEXT_LETTERS_AMOUNT]


class UserProjectStatistics(models.Model):
    choice_values = ((True, 'Да'), (False, 'Нет'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user_statistics')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_statistics')
    is_created_project = models.BooleanField('Проект создан этим автором?', default=False,
                                             choices=choice_values)
    is_liked_project = models.BooleanField('Пользователь поставил звезду проекту?', default=False,
                                           choices=choice_values)
    is_saved_project = models.BooleanField('Пользователь добавил проект в закладки', default=False,
                                           choices=choice_values)
    views_amount = models.IntegerField('Количество просмотров проекта', default=0)
    last_visit_date = models.DateTimeField('Дата последнего просмотра проекта', auto_now=True)

    class Meta:
        verbose_name = 'Статистика пользователя'
        verbose_name_plural = 'Статистика пользователей'
