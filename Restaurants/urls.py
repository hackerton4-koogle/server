from django.urls import path
from . import views

urlpatterns = [
    path('api/food/<int:food_id>/restaurants/', views.get_restaurants_by_food),
    path('', views.main_page, name='main_page'),
    path('search/', views.search_restaurants, name='search_restaurants'), #검색
]