from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

TITLE_PREVIEW_LENGTH = 50

User = get_user_model()


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено')

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_query_name='post_author'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_query_name='post_location'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_query_name='post_category'
    )

    def get_posts(**filters):
        filters_dict = {
            'is_published': True,
            'pub_date__lte': timezone.now(),
            'category__is_published': True
        }
        filters_dict.update(filters)
        return Post.objects.filter(**filters_dict)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        if len(self.title) > TITLE_PREVIEW_LENGTH:
            return self.title[:TITLE_PREVIEW_LENGTH] + '...'
        else:
            return self.title


class Category(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if len(self.title) > TITLE_PREVIEW_LENGTH:
            return self.title[:TITLE_PREVIEW_LENGTH] + '...'
        else:
            return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        if len(self.name) > TITLE_PREVIEW_LENGTH:
            return self.name[:TITLE_PREVIEW_LENGTH] + '...'
        else:
            return self.name
