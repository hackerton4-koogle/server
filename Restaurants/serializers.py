import geopy
from rest_framework import serializers

from Users.models import User
from .models import *

# 이름, 쿠글, 카테고리, 음식, 전화번호, 주소, 오픈, 클로즈 시간, 예약 유무, 가게 사진 필요
class RestaurantBaseSerializer(serializers.ModelSerializer):
    koogle_rating = serializers.IntegerField(source='koogle_ranking')
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'address',
            'image',
            'phone',
            'map_link',
            'latitude',
            'longitude',
            'koogle_rating',
            'reservation',
            'reservation_link',
        )

class DistanceMixin():
    def get_distance(self, restaurant):
        user_coords = (self.context.get('user_y'), self.context.get('user_x'))
        restaurant_coords = (restaurant.latitude, restaurant.longitude)

        if None in user_coords or None in restaurant_coords:
            return None
        
        return int(geopy.distance.distance(user_coords, restaurant_coords).m)

class RestaurantSerializer(DistanceMixin, RestaurantBaseSerializer):
    distance = serializers.SerializerMethodField()
    review_cnt = serializers.ReadOnlyField(source='review_count')
    class Meta(RestaurantBaseSerializer.Meta):
        fields = RestaurantBaseSerializer.Meta.fields + (
            'distance',
            'review_cnt',
        )
