from django.contrib import admin
from .models import Ingredients , Purchases , Recipes , RecipeIngredients , stock
# Register your models here.
admin.site.register(Ingredients)
admin.site.register(Purchases)
admin.site.register(Recipes)
admin.site.register(RecipeIngredients)
admin.site.register(stock)