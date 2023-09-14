from django.urls import path
from .views import *

urlpatterns =[
    path('', SelectedFoodsRestaurantsView.as_view()),
    path('<int:pk>', RestaurantView.as_view()),
    path('search/', search_restaurants, name='search_restaurants'), #검색
]