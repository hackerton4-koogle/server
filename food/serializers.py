from rest_framework import serializers

from Restaurants.models import Category, Food
from translation.utils import translate

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = (
            'id', 
            'name',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = translate(ret['name'])

        return ret

class CategorySerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True, read_only=True, source='food_category')

    class Meta:
        model = Category
        fields = (
            'name', 
            'foods',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = translate(ret['name'])

        return ret