from django.core.management.base import BaseCommand
import csv
from reviews.models import Category, Genre, Title, TitleGenre


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
        self.stdout.write('Выполнение команды продолжено.')
        tables = (
            ('category', Category, ('id', 'name', 'slug')),
            ('genre', Genre, ('id', 'name', 'slug')),
            # ('titles', Title, ('id', 'name', 'year', 'category')),
            # ('genre_title', TitleGenre, ('id', 'title_id', 'genre_id')),
        )
        for table in tables:
            file_name = table[0]
            model_name = table[1]
            field_names = table[2]
            model_name.objects.all().delete()
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
