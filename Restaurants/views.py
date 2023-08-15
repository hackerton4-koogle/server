from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Food, Restaurant
from .serializers import RestaurantSerializer

from django.contrib.gis.geos import Point #pip install geopy
from geopy.distance import great_circle
from django.contrib.gis.measure import Distance

@api_view(['POST'])
def get_restaurants_by_selected_items(request):
    selected_items = request.data.get('selected_items', [])
    sort_by = request.data.get('sort_by')

    if not selected_items:
        return Response({"error": "No selected items provided"}, status=400)

    
    user_latitude = request.data.get('latitude')  # 사용자 위치의 위도
    user_longitude = request.data.get('longitude')  # 사용자 위치의 경도
    user_location = Point(user_longitude, user_latitude) 

    restaurants = Restaurant.objects.filter(
        restaurant_food__food__id__in=selected_items
    )

    #거리순 정렬
    if sort_by == 'distance':
        restaurants = sorted(
            restaurants,
            key=lambda restaurant: great_circle(
                (restaurant.latitude, restaurant.longitude),
                (user_latitude, user_longitude)
            ).meters
        )
        # 거리를 계산하여 응답 데이터에 추가
        serialized_data = []
        for restaurant in restaurants:
            distance = great_circle(
                (restaurant.latitude, restaurant.longitude),
                (user_latitude, user_longitude)
            ).meters
            serialized_data.append({
                "restaurant_info": RestaurantSerializer(restaurant).data,
                "distance": distance  # 거리 정보를 추가
            })

    #평점순 정렬
    if sort_by == 'rating':
        restaurants = restaurants.order_by('-koogle_ranking')

    serialized_data = RestaurantSerializer(restaurants, many=True).data
    return Response(serialized_data)


from django.shortcuts import render
from .models import Category

def main_page(request):
    categories = Category.objects.all()
    return render(request, 'main_page.html', {'categories': categories})