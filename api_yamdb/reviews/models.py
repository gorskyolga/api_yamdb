from django.db import models
from django.db.models import Avg
from django.db.models.constraints import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

from api.validators import validate_year
from api_yamdb.settings import SCORE_MAXVALUE, SCORE_MINVALUE
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название категории',
        help_text='Длина не более 255 символов.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        help_text=('Уникальное поле. Длина не более 50 символов. Допустимые '
                   'символы: -, _, латинские буквы, цифры.')
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название жанра',
        help_text='Длина не более 255 символов.'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
        help_text=('Уникальное поле. Длина не более 50 символов. Допустимые '
                   'символы: -, _, латинские буквы, цифры.')
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название произведения',
        help_text='Длина не более 255 символов.'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Год выпуска не может быть больше текущего.',
        validators=(MinValueValidator(0), validate_year)
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Не обязательное поле. Значение по умолчание - пусто.',
        blank=True,
        default=''
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', related_name='titles',
        verbose_name='Жанр произведения',
        help_text='Жанр произведения из существующих жанров.'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        help_text='Категория произведения из существующих категорий.',
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Название произведения',
                              help_text='Длина не более 255 символов.')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Название жанра',
                              help_text='Длина не более 255 символов.')

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва', help_text='Автор отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которому относится отзыв')
    text = models.TextField(
        verbose_name='Текст отзыва', help_text='Напишите отзыв'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(SCORE_MINVALUE),
                    MaxValueValidator(SCORE_MAXVALUE),),
        verbose_name='Оценка произведения',
        help_text='Укажите оценку')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True,
        help_text='Дата добавления отзыва')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            UniqueConstraint(fields=('title', 'author',),
                             name='unique_review'),
        )

    def __str__(self):
        return self.text

    def calc_title_rating(self):
        rating = self.reviews.aggregate(Avg('score'))['score__avg']
        if rating is not None:
            return round(rating, 0)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария', help_text='Автор комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которому относится комментарий')
    text = models.TextField(
        verbose_name='Текст комментария', help_text='Напишите комментарий'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True,
        help_text='Дата добавления комментария')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
