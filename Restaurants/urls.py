from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views
router = DefaultRouter()


urlpatterns =[
    path('food/<str:food_ids>/restaurants/', FoodSelectedRestaurantsAPIView.as_view()),
    path('', MainpageAPIView.as_view(), name='main_page'),
    path('<str:restaurant_name>/', RestaurantsBaseAPIView.as_view()),
    path('search/', views.search_restaurants, name='search_restaurants'), #검색
]