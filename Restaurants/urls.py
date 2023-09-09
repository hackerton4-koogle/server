from django.urls import path
from .views import *

urlpatterns =[
    path('food/<str:food_id>/restaurants/', FoodSelectedRestaurantsAPIView.as_view()),
    path('<str:restaurant_name>/', RestaurantsBaseAPIView.as_view()),
    path('search/', search_restaurants, name='search_restaurants'), #검색
]