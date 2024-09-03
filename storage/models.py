from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Purpose: To store details about each ingredient.
class Ingredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1 ,verbose_name='User')  
    name = models.CharField( max_length=100)
    Category = models.CharField(max_length=100)
    UnitOfMeasure = models.CharField(max_length=50)
    ingredients_size =models.FloatField(null=True )
    def __str__(self):
        return self.name


         
class stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1 ,verbose_name='User')  
    IngredientID = models.ForeignKey(Ingredients, on_delete=models.CASCADE ,default=1)
    Quantity = models.FloatField()
    def __str__(self):
        return f"{self.IngredientID.name} - Quantity: {self.Quantity}"

class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1 ,verbose_name='User')  
    IngredientID = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    PurchaseDate = models.DateField(auto_now=False, auto_now_add=False)
    Quantity = models.FloatField()
    ExpiryDate = models.DateField(default='2026-12-25', auto_now=False, auto_now_add=False)
    def __str__(self):
        return str(self.IngredientID.name)


class Recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1,verbose_name='User')  
    necipes_name = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)
    img = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None ,null=True)
    def __str__(self):
        return f"{self.necipes_name}"
    


# Purpose: To link ingredients to recipes and specify amounts used.
class RecipeIngredients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1,verbose_name='User')  
    RecipeID = models.ForeignKey( Recipes, on_delete=models.CASCADE)
    IngredientID = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    Quantity = models.FloatField()
    def __str__(self): 
        return f"{self.IngredientID.name} - في: {self.RecipeID.necipes_name}" 
    






