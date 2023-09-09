from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from food.serializers import CategorySerializer

from Restaurants.models import Category

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.all().prefetch_related('food_category')