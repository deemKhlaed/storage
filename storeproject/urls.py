"""
URL configuration for storeproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from storage import views as store
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,store.index, name= 'index') ,
    path('createR/', store.create_recipe , name= 'createRecipe'),
    path('purchase/', store.purchase_ingredient ,name='purchase'),
    path('login/',store.auth_login , name='login'),
    path('auth_register/',store.auth_register,name='auth_register'),
    path('addRecipeIngredients/<int:id>/',store.addRecipeIngredients ,name='addRecipeIngredients' ),
    path('recipes/' , store.displayRecipe , name="recipes"),
    path('logout/' , store.logoutUser , name='logout'),
    path("editR/", store.editR ,),
    path("updateR/", store.updateRecipe ,),
    path("deleteR/", store.deleteRecipe),
    path('chart/', store.chart,name='chart')




]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

