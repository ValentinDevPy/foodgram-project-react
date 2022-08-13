from django.contrib import admin

from recipes.models import RecipeTag, Tag, Ingredient, Favorite, RecipeIngredient, Recipe

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredient)