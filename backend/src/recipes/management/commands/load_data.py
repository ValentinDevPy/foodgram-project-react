import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("data/ingredients.json", "rb") as f:
            data = json.load(f)
            for elem in data:
                ingredient = Ingredient()
                ingredient.name = elem["name"]
                ingredient.measurement_unit = elem["measurement_unit"]
                ingredient.save()

        with open("data/tags.json", "rb") as f:
            data = json.load(f)
            for elem in data:
                tag = Tag()
                tag.name = elem["name"]
                tag.color = elem["color"]
                tag.slug = elem["slug"]
                tag.save()
