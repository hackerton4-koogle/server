from rest_framework import serializers
from django.db.models import Count

from Restaurants.models import *
from Reviews.models import Likes, Review, Review_Likes
from Users.models import User

import geopy
from translation.utils import translate

class TranslationMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = self.context.get('language', '영어')

    def translate_dict(self, data, keys):
        for key in keys:
            if key in data:
                data[key] = translate(data[key], self.language)
        return data
    
    def translate_list(self, data):
        ret = []
        for item in data:
            ret.append(translate(item, self.language))
        return ret
    
    def translate_list_of_dict(self, data, keys):
        ret = []
        for item in data:
            for key in keys:
                if key in item:
                    item[key] = translate(item[key], self.language)
            
            ret.append(item)
        
        return ret


class RestaurantBaseSerializer(TranslationMixin, serializers.ModelSerializer):
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

    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)
        instance_dict = self.translate_dict(instance_dict, ['name', 'address'])

        return instance_dict

class DistanceMixin:
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

class RestaurantDetailedInfoSerializer(DistanceMixin, RestaurantBaseSerializer):
    distance = serializers.SerializerMethodField()
    restaurant_map_url = serializers.ReadOnlyField(source='map_link')
    distance = serializers.SerializerMethodField()

    class Meta(RestaurantBaseSerializer.Meta):
        fields_list = list(RestaurantBaseSerializer.Meta.fields)
        fields_list.remove('map_link')

        fields = tuple(fields_list) + (
            'distance', 
            'restaurant_map_url', 
            'categories', 
            'naver_koogle', 
            'user_koogle', 
            'naver_likes_data', 
            'user_likes_data', 
            'restaurant_menu', 
            'opening_closing_time',
        )

    categories = serializers.SerializerMethodField()

    def get_categories(self, restaurant):
        restaurant_foods = Restaurant_Food.objects.filter(restaurant=restaurant)
        categories = Food.objects.filter(restaurant_food_food__in=restaurant_foods).values_list('category__name', flat=True)

        return categories
        

    naver_koogle = serializers.SerializerMethodField()

    def get_naver_koogle(self, restaurant):
        naver_users = User.objects.filter(is_staff=True)
        naver_reviews = Review.objects.filter(user__in=naver_users, restaurant=restaurant)

        return self._get_koogle(naver_reviews)
    
    user_koogle = serializers.SerializerMethodField()

    def get_user_koogle(self, restaurant):
        koogle_users = User.objects.filter(is_staff=False)
        koogle_reviews = Review.objects.filter(user__in=koogle_users, restaurant=restaurant)

        return self._get_koogle(koogle_reviews)

    def _get_koogle(self, reviews):
        reviews_likes_cnt = Review_Likes.objects.filter(review__in=reviews).count()
        reviews_cnt = reviews.count()

        from Restaurants.views import koogle_cal
        return koogle_cal(reviews_likes_cnt, reviews_cnt)

    naver_likes_data = serializers.SerializerMethodField()

    def get_naver_likes_data(self, restaurant):
        naver_users = User.objects.filter(is_staff=True)
        naver_reviews = Review.objects.filter(user__in=naver_users, restaurant=restaurant)

        likes_counts = (
            Likes.objects.filter(likes_review_likes__review__in=naver_reviews)
            .annotate(count=Count('likes_review_likes'))
            .values('likes', 'count')
        )

        return likes_counts
    
    user_likes_data = serializers.SerializerMethodField()

    def get_user_likes_data(self, restaurant):
        koogle_users = User.objects.filter(is_staff=False)
        koogle_reviews = Review.objects.filter(user__in=koogle_users, restaurant=restaurant)

        likes_counts = (
            Likes.objects.filter(likes_review_likes__review__in=koogle_reviews)
            .annotate(count=Count('likes_review_likes'))
            .values('likes', 'count')
            .order_by('-count')
        )

        return likes_counts
    
    restaurant_menu = serializers.SerializerMethodField()

    def get_restaurant_menu(self, restaurant):
        menus = Menu.objects.filter(restaurant=restaurant)
        menu_details = Menu_Detail.objects.filter(menu__in=menus)
        
        return MenuDetailSerializer(menu_details, many=True).data
    
    opening_closing_time = serializers.SerializerMethodField()

    def get_opening_closing_time(self, restaurant):
        open_hours = OpenHours.objects.filter(restaurant=restaurant)

        return OpenHourSerializer(open_hours, many=True).data
    
    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)
        instance_dict['categories'] = self.translate_list(instance_dict['categories'])

        instance_dict['user_likes_data'] = self.translate_list_of_dict(instance_dict['user_likes_data'], ['likes'])
        instance_dict['naver_likes_data'] = self.translate_list_of_dict(instance_dict['naver_likes_data'], ['likes'])

        instance_dict['opening_closing_time'] = self.translate_list_of_dict(instance_dict['opening_closing_time'], ['day'])

        instance_dict['restaurant_menu'] = self.translate_list_of_dict(instance_dict['restaurant_menu'], ['name', 'content'])

        return instance_dict


class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_Detail
        fields = (
            'name', 
            'price', 
            'image',
            'content',
        )


class OpenHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenHours
        fields = (
            'day', 
            'open_time', 
            'close_time',
        )

    def to_representation(self, instance):
        instance_dict = super().to_representation(instance)

        from datetime import datetime

        open_time = datetime.strptime(instance_dict['open_time'], '%H:%M:%S')
        instance_dict['open_time'] = open_time.strftime('%I:%M %p')

        close_time = datetime.strptime(instance_dict['close_time'], '%H:%M:%S')
        instance_dict['close_time'] = close_time.strftime('%I:%M %p')

        return instance_dict
