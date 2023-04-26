import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):
    help = 'Import initial data from csv-files to DB'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'Выполнение команды приведёт к удалению существующих записей в'
                ' БД. Нажмите 1, если хотите продолжить выполнение команды.'
            )
        )
        if input() != '1':
            self.stdout.write('Выполнение команды остановлено.')
            return
        [model_name.objects.all().delete() for model_name in (
            Category, Comment, Genre, Review, Title, TitleGenre, User
        )]
        self.stdout.write('Таблицы базы данных очищены.')

        models_info = (
            ('category', Category, ('id', 'name', 'slug')),
            ('genre', Genre, ('id', 'name', 'slug')),
            ('users', User, ('id', 'username', 'email', 'role', 'bio',
                             'first_name', 'last_name')),
        )
        for file_name, model_name, field_names in models_info:
            with open(
                f'static/data/{file_name}.csv', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    new_object = model_name()
                    for field in field_names:
                        new_object.__setattr__(field, row[field])
                    new_object.save()
            self.stdout.write(
                f'Даннные модели {model_name.__name__} загружены.'
            )

        with open('static/data/titles.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                Title.objects.create(
                    id=row['id'], name=row['name'], year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
            self.stdout.write('Даннные модели Title загружены.')

        with open('static/data/genre_title.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                TitleGenre.objects.create(
                    id=row['id'], title=Title.objects.get(id=row['title_id']),
                    genre=Genre.objects.get(id=row['genre_id'])
                )
            self.stdout.write('Даннные модели TitleGenre загружены.')

        with open('static/data/review.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                obj = Review.objects.create(
                    id=row['id'], title=Title.objects.get(id=row['title_id']),
                    text=row['text'], score=row['score'],
                    author=User.objects.get(id=row['author'])
                )
                obj.pub_date = row['pub_date']
                obj.save()
            self.stdout.write('Даннные модели Review загружены.')

        with open('static/data/comments.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                obj = Comment.objects.create(
                    id=row['id'], text=row['text'],
                    review=Review.objects.get(id=row['review_id']),
                    author=User.objects.get(id=row['author'])
                )
                obj.pub_date = row['pub_date']
                obj.save()
            self.stdout.write('Даннные модели Comment загружены.')
