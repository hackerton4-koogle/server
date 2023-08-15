from rest_framework import serializers
from .models import Category, Food, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

# 다른 직렬화 클래스들도 동일한 방식으로 작성
