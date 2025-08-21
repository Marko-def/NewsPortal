from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from NewsPaper import News
from django.utils import timezone


class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории после подтверждения'

    def add_arguments(self, parser):
        parser.add_argument('category_id', type=int, help='ID категории новостей для удаления')

    def handle(self, *args, **kwargs):
        category_id = kwargs['category_id']

        # Подтверждение действия
        confirmation = input(f'Вы уверены, что хотите удалить все новости из категории с ID {category_id}? (да/нет): ')

        if confirmation.lower() == 'да':
            try:
                # Удаление новостей из указанной категории
                deleted_count, _ = News.objects.filter(category_id=category_id).delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Успешно удалено {deleted_count} новостей из категории с ID {category_id}.'))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория с ID {category_id} не найдена.'))
        else:
            self.stdout.write(self.style.WARNING('Удаление новостей отменено.'))