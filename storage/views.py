from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse
from .models import Ingredients  , stock , RecipeIngredients ,Recipes , Purchases
from django.template import loader
from django.forms import modelformset_factory 
from django.views.decorators.csrf import csrf_exempt
from .forms import IngredientsForm , PurchasesForm , RecipesForm, RecipeIngredientsForm ,CreateUserForm,LoginUserForm
from django.contrib.auth import login , authenticate , logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@csrf_exempt
def auth_login(request):
     if request.user.is_authenticated:
         return redirect('/')
     form=LoginUserForm()
     if request.method == "POST":
          form=LoginUserForm(data=request.POST)
          if form.is_valid():  
              username=form.cleaned_data['username']
              password=form.cleaned_data['password']
              user=authenticate(request=request,username=username,password=password)
              if user:
                   if user.is_active:         
                        login(request=request,user=user)
                        request.session["name"]= username
                        return redirect('index')
          else:
             context={'form':form ,'show_login_modal': True}
             return render(request,'auth/auth_login.html',context)            
     context={'form':form }
     return render(request,'auth/auth_login.html',context)

@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('login')
@csrf_exempt
def auth_register(request):
    if request.user.is_authenticated:
      return redirect('/')
    
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('/')
    
    context={'form':form}
    return render(request,'auth/auth_register.html',context)
   
@csrf_exempt
def editR(request):
    p = Recipes.objects.filter( id=request.POST.get('id'))   
    for item in p:
            value = {
            'id':item.id  ,  
            'RecipesName': item.necipes_name,
            'description': item.Description  
        }
    return JsonResponse({'value':value})

@login_required(login_url="/login/")
@csrf_exempt
def index(request):
    if request.method == 'POST':
        fIngredientsForm = IngredientsForm(request.POST)
        if fIngredientsForm.is_valid():
            ingredient = fIngredientsForm.save(commit=False)
            ingredient.user = request.user  # Add user here
            ingredient.save()
            return redirect('/')
    
    dataPurchases = Purchases.objects.filter(user=request.user)  # Filter by user
    dataInventory = stock.objects.filter(user=request.user)  # Filter by user
    ls = needToBuyList(user=request.user)
    fIngredientsForm = IngredientsForm()
    forms = {
        'Ingredients': fIngredientsForm,
    }
    templates = loader.get_template('index.html')
    return HttpResponse(templates.render({'form': forms, 'Inventory': dataInventory, 'request': request, 'Purchases': dataPurchases ,'listToBuy':ls}))


@login_required(login_url="/login/")
@csrf_exempt
def create_recipe(request):
    if request.method == "POST":
        fRecipesForm = RecipesForm(request.POST ,request.FILES)
        if fRecipesForm.is_valid():
            recipe = fRecipesForm.save(commit=False)
            recipe.user = request.user  # Add user here
            recipe.save()
            return redirect('addRecipeIngredients', id=recipe.id)
    else:
        fRecipesForm = RecipesForm()
    forms = {
        'Recipes': fRecipesForm,
    }
    templates = loader.get_template('create_recipe.html')
    return HttpResponse(templates.render({'form': forms, 'request': request}))


@login_required(login_url="/login/")
@csrf_exempt
def addRecipeIngredients(request, id):
    recipe_instance = get_object_or_404(Recipes, pk=id)
    RecipeIngredientsFormSet = modelformset_factory(RecipeIngredients, form=RecipeIngredientsForm, extra=5)

    if request.method == 'POST':
        formset = RecipeIngredientsFormSet(request.POST ,form_kwargs={'user': request.user})
        if formset.is_valid():
            for form in formset:
                ingredient = form.save(commit=False)
                ingredient.RecipeID = recipe_instance
                ingredient.user = request.user 
                ingredient.save()
            return redirect('recipes')
    else:
        formset = RecipeIngredientsFormSet(queryset=RecipeIngredients.objects.none(),form_kwargs={'user': request.user})

    template = loader.get_template('addRecipeIngredients.html')
    return HttpResponse(template.render({'formset': formset, 'request': request, 'Recipenme': recipe_instance.necipes_name}))


@login_required(login_url="/login/")
@csrf_exempt
def purchase_ingredient(request):
    if request.method == 'POST':
        form = PurchasesForm(request.POST , user=request.user )
        if form.is_valid():
            # Save the purchase data
            purchase = form.save(commit=False)
            purchase.user = request.user  # Add user here
            purchase.save()

            # Get or create the corresponding Inventory record
            updateStock, created = stock.objects.get_or_create(
                IngredientID=purchase.IngredientID,
                defaults={'Quantity': 0, 'user': request.user}  # Add user here
            )
            
            # Update the inventory quantity
            updateStock.Quantity += purchase.Quantity
            updateStock.save()
            messages.success(request,  'تم اضافة '+ (purchase.IngredientID.name) +' بنجاح ' )

            # Redirect to a success page or return a response
            return redirect('/purchase/')  # Replace 'success_url' with your actual success URL
    else:
        form = PurchasesForm(user=request.user)

    return render(request, 'purchase_ingredient.html', {'form': form})


@login_required(login_url="/login/")
def displayRecipe(request):
    recipes = Recipes.objects.filter(user=request.user)  # Filter by user
    recipe_details = []
    for recipe in recipes:
        ingredients = RecipeIngredients.objects.filter(RecipeID=recipe, user=request.user)  # Filter by user
        recipe_details.append({
            'recipe': recipe,
            'ingredients': ingredients,
        })
    template = loader.get_template('display_resipe.html')
    return HttpResponse(template.render({'request': request, 'recipe_details': recipe_details}))

@login_required(login_url="/login/")
@csrf_exempt
def updateRecipe(request):
    id = request.POST.get('id')
    name= request.POST.get('Recipename')
    image=request.POST.get('img')
    description=request.POST.get('description')   
    try:
            recipe = Recipes.objects.get(id=id)

            recipe.necipes_name = name
            recipe.Description = description
            if image:
                recipe.img = 'images/'+image  
            recipe.save()  

            return redirect('/recipes/')
    except Recipes.DoesNotExist:
        pass
    return redirect('/recipes/') 

@login_required(login_url="/login/")
@csrf_exempt
def deleteRecipe(request):
    recipe = Recipes.objects.get(id=request.POST.get('id'))
    recipe.delete()
    return redirect('/recipes/') 



@login_required(login_url="/login/")
def updateStock(request):
    # 
    orders = [
        {
    'recipes_name':'برقر',
    'Qty':1
     }
    ]
    for order in orders:
        getRecipe = Recipes.objects.get(necipes_name = order['recipes_name'] ,user=request.user)
        ingredients = RecipeIngredients.objects.filter(RecipeID=getRecipe, user=request.user)  
        for i in range(order['Qty']):
             for ingredient in ingredients:
                ingredient_stock = stock.objects.get(IngredientID= ingredient.IngredientID)
                if ingredient.Quantity <= ingredient_stock.Quantity:
                    ingredient_stock.Quantity -= ingredient.Quantity 
                    ingredient_stock.save()
                else:
                    pass
    return redirect('/')        

       
def needToBuyList(user):
    stock_ = stock.objects.filter(user=user)
    ls = []
    for item  in stock_:
        if item.Quantity <= 0:
            ls.append('نفذ  '+str(item.IngredientID))
    return ls


        
@login_required(login_url="/login/")
@csrf_exempt
def chart(request):
    stock_ = stock.objects.filter(user=request.user)
    names = [item.IngredientID.name for item in stock_]
    quantities = [item.Quantity for item in stock_]
    chart_data = {
        'names': names,
        'quantities': quantities
    }
    template = loader.get_template('chart.html')
    return HttpResponse(template.render({'chart_data':chart_data ,'request':request}))





    



    

    