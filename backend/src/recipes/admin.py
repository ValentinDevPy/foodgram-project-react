from django.contrib import admin

from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "author"]
    list_filter = ["author", "name", "tags"]
    filter_horizontal = ("ingredients",)
    readonly_fields = ["added_to_favorite"]
    inlines = [IngredientInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "measurement_unit"]
    list_filter = ["name"]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(RecipeIngredient)
