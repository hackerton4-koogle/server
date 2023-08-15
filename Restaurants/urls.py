from django.urls import path
from . import views

urlpatterns = [
    path('api/food/<int:food_id>/restaurants/', views.get_restaurants_by_food),
    path('', views.main_page, name='main_page'),
    # 다른 URL 패턴들도 추가
]