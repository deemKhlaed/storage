from django.db import models
from storage.models import Recipes,RecipeIngredients,stock
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class Dishes(models.Model):
    provider = models.CharField(max_length=50,null=True)
    dish_name = models.CharField(max_length=50)
    price = models.FloatField(null=True)
    # save and update stock
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = get_object_or_404(User, username=self.provider)
    
        try:
          getRecipe = Recipes.objects.get(necipes_name=self.dish_name, user=user)
          ingredients = RecipeIngredients.objects.filter(RecipeID=getRecipe, user=user)
          
        
          for ingredient in ingredients:
            try:
                ingredient_stock = stock.objects.get(IngredientID=ingredient.IngredientID)
                if ingredient.Quantity <= ingredient_stock.Quantity:
                    ingredient_stock.Quantity -= ingredient.Quantity
                    ingredient_stock.save()
                else:
                    print(f"Insufficient stock for IngredientID: {ingredient.IngredientID}")
            except stock.DoesNotExist:
                print(f"Stock not found for IngredientID: {ingredient.IngredientID}")
        except Recipes.DoesNotExist:
                print(f"Recipe not found for dish_name: {self.dish_name} and provider: {self.provider}")
