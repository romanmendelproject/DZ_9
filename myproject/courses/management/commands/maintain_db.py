import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from faker import Faker
from courses.models import Teacher, Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        faker = Faker(locale='en_US')

        for _ in range(5):
            first_name = faker.first_name(),
            User_item = User.objects.create(
                    first_name=first_name[0],
                    last_name=faker.last_name(),
                    username=first_name[0][:4],
                )
            Teacher.objects.create(
                user=User_item,
                sex=random.choice(['m', 'f']),
                bio=faker.text(max_nb_chars=1000, ext_word_list=None),
                city=faker.city(),
                date_of_birth=faker.date(),
            )

        for _ in range(20):
            first_name = faker.first_name(),
            User_item = User.objects.create(
                    first_name=first_name[0],
                    last_name=faker.last_name(),
                    username=first_name[0][:4],
                )
            Student.objects.create(
                user=User_item,
                sex=random.choice(['m', 'f']),
                city=faker.city(),
                date_of_birth=faker.date(),
            )