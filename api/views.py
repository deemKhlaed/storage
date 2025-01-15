from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import DishesSerializer
from storage.models import Recipes
@api_view(['GET'])
def getRecipes(request):
    orders = Recipes.objects.all()
    serislizer = DishesSerializer(orders,many=True)
    return Response(serislizer.data)

@api_view(['POST'])
def getOrder(request):
    serislizer = DishesSerializer(data=request.data)
    if serislizer.is_valid():
        serislizer.save()
    else:
        print("not valid")    
    return Response(serislizer.data)