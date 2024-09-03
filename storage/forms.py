from django import forms
from django.forms import ModelForm , inlineformset_factory ,BaseInlineFormSet
from .models import Ingredients , Purchases ,Recipes , RecipeIngredients
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='اسم المستخدم')
    email = forms.EmailField(label='الايميل')
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']


UnitOfMeasure_CHOICES = [
    ('kg', 'كيلو'),
    ('l', 'لتر'),
    ('g', 'جرام'),
    ('ml', 'ملليتر'),
    ('unit', 'حبات'),
]

class IngredientsForm(ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name', 'Category', 'UnitOfMeasure', 'ingredients_size']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'Category': forms.TextInput(attrs={'class': 'form-control'}),
            'UnitOfMeasure': forms.Select(choices=UnitOfMeasure_CHOICES, attrs={'class': 'form-control'}),
            'ingredients_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'الاسم',
            'Category': 'الفئة',
            'UnitOfMeasure': 'وحدة القياس',
            'ingredients_size': 'حجم المنتج',
        }






class PurchasesForm(ModelForm):
    class Meta:
        model = Purchases
        fields = ['IngredientID', 'PurchaseDate', 'Quantity' ,'ExpiryDate']
        widgets = {
            'IngredientID': forms.Select(attrs={'class': 'form-select'}),
            'PurchaseDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'ExpiryDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
        labels = {
            'IngredientID': 'اسم المنتج',
            'PurchaseDate': 'تاريخ الشراء',
            'Quantity': 'الكمية',
            'ExpiryDate':'تاريخ الانتهاء'
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from the kwargs
        super(PurchasesForm, self).__init__(*args, **kwargs)
        if user:
             self.fields['IngredientID'].queryset = Ingredients.objects.filter(user=user)


class RecipesForm(ModelForm):
    class Meta:
        model = Recipes
        fields = ['necipes_name', 'Description' ,'img']
        widgets = {
            'necipes_name': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'Description': forms.Textarea(attrs={'class': 'form-control mt-2'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control mt-2', 'required': False}),

        }
        labels = {
            'necipes_name': 'اسم الوصفة',
            'Description': 'طريقة التحضير',
            'img':'صورة'
        }
        

    
class RecipeIngredientsForm(ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['IngredientID', 'Quantity']
        widgets = {
            'IngredientID': forms.Select(attrs={'class': 'form-select-sm-3 form-inline '}),
            'Quantity': forms.NumberInput(attrs={'class': 'form-control-sm-3  '}),
        }
        labels = {
            'IngredientID': ' المنتج',
            'Quantity': 'الكمية',
        }
    def __init__(self, *args, **kwargs):
        self.RecipeID = kwargs.pop('RecipeID', None)
        user = kwargs.pop('user', None)
        super(RecipeIngredientsForm, self).__init__(*args, **kwargs)
        if user:
             self.fields['IngredientID'].queryset = Ingredients.objects.filter(user=user)
    
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['id_RecipeID'] = self.RecipeID
        return cleaned_data   

        

RecipeIngredientsFormset = inlineformset_factory(
    Recipes, RecipeIngredients, form=RecipeIngredientsForm, extra=2,min_num=1, validate_min=True
    , can_delete=False
)

