from django.contrib import admin

from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(RecipeIngredient)