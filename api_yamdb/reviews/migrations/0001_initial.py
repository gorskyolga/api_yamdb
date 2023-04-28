# Generated by Django 3.2 on 2023-04-28 20:12

import api.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Длина не более 255 символов.', max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Уникальное поле. Длина не более 50 символов. Допустимые символы: -, _, латинские буквы, цифры.', unique=True, verbose_name='Слаг категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Напишите комментарий', verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата добавления комментария', verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Длина не более 255 символов.', max_length=255, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='Уникальное поле. Длина не более 50 символов. Допустимые символы: -, _, латинские буквы, цифры.', unique=True, verbose_name='Слаг жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Напишите отзыв', verbose_name='Текст отзыва')),
                ('score', models.PositiveSmallIntegerField(help_text='Укажите оценку', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка произведения')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата добавления отзыва', verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Длина не более 255 символов.', max_length=255, verbose_name='Название произведения')),
                ('year', models.PositiveSmallIntegerField(help_text='Год выпуска не может быть больше текущего.', validators=[django.core.validators.MinValueValidator(0), api.validators.validate_year], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, default='', help_text='Не обязательное поле. Значение по умолчание - пусто.', verbose_name='Описание произведения')),
                ('category', models.ForeignKey(blank=True, help_text='Категория произведения из существующих категорий.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория произведения')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('year',),
            },
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(help_text='Длина не более 255 символов.', on_delete=django.db.models.deletion.CASCADE, to='reviews.genre', verbose_name='Название жанра')),
                ('title', models.ForeignKey(help_text='Длина не более 255 символов.', on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='Название произведения')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(help_text='Жанр произведения из существующих жанров.', related_name='titles', through='reviews.TitleGenre', to='reviews.Genre', verbose_name='Жанр произведения'),
        ),
    ]
