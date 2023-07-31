from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    help = 'Load data from CSV file into the Ingredient model.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                name = row[0]
                measurement_unit = row[1]

                ingredient = Ingredient(name=name,
                                        measurement_unit=measurement_unit)
                ingredient.save()

        self.stdout.write('Data imported successfully.')
