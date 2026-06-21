from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    list_filter = ['category']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'source', 'calories', 'is_favorite', 'rating', 'created_at']
    list_filter = ['source', 'is_favorite', 'tags']
    filter_horizontal = ['tags']
    inlines = [IngredientInline]
