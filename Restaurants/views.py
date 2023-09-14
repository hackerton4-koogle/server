from django.db.models import Count
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from Restaurants.models import *
from Restaurants.serializers import *
from Reviews.models import *

from translation.utils import translate
import geopy.distance

# 이름, 전화번호, 주소, 오픈, 클로즈 시간, 예약 유무, 가게 사진 필요
# 현재 내위치가 가게로 부터 몇미터 떨어져 있는지 -> 계산 필요
# 몇 쿠글로 예상이 되는지 -> 계산 필요 ( 유저와 네이버를 통해서 각각 )
# 

def translate_data(data):
    translated_data = {}

    for key, value in data.items():
        if isinstance(value, str):  # 문자열인 경우에만 번역 수행
            translated_text = translate(value)
            translated_data[key] = translated_text if translated_text is not None else value  # 수정된 부분
        elif isinstance(value, dict):  # 중첩된 딕셔너리인 경우 재귀적으로 번역 수행
            translated_data[key] = translate_data(value)
        else:
            translated_data[key] = value  # 문자열이 아닌 경우 그대로 유지

    return translated_data

class SelectedFoodsRestaurantsView(generics.ListAPIView):
        queryset = Restaurant.objects.all()
        serializer_class = RestaurantSerializer
        permission_classes = [AllowAny]

        allowed_sort_criteria = ['distance', 'rating', 'review']
        default_location = (37.5508, 126.9255)

        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'request': self.request,
                'user_y' : float(self.request.query_params.get('y', self.default_location[0])),
                'user_x' : float(self.request.query_params.get('x', self.default_location[1])),
            }
        
        def get_queryset(self):
            sort_criteria = self.request.query_params.get('sort')

            # Get list of Food ids from query parameter and convert them into list.
            food_ids = self.request.query_params.get('food_ids')
            food_ids = [int(id) for id in food_ids.split(',')]

            # Fetch all restaurants related to these food items.
            queryset = Restaurant.objects.filter(restaurant_food_restaurant__food__id__in=food_ids)

            if sort_criteria == "distance":
                queryset = list(queryset)

                user_y = float(self.request.query_params.get('y', self.default_location[0]))
                user_x = float(self.request.query_params.get('x', self.default_location[1]))

                queryset.sort(key=lambda x: geopy.distance.distance((x.latitude,x.longitude),(user_y, user_x)).m)
            elif sort_criteria == "rating":
                queryset = queryset.order_by('-koogle_ranking')
            elif sort_criteria == "review":
                queryset = queryset.annotate(review_count=Count('review_restaurant')).order_by('-review_count')

            return queryset
        
        def list(self, request, *args, **kwargs):
            # Get sort criteria from query parameters. If it doesn't exist or is invalid,
            # respond with an error.
            sort_criteria = self.request.query_params.get('sort')
            if sort_criteria is None or sort_criteria not in self.allowed_sort_criteria:
                return Response({"error": "Invalid or missing sort criteria. Must be one of: " + ', '.join(self.allowed_sort_criteria)}, status=status.HTTP_400_BAD_REQUEST)
            
            food_ids = self.request.query_params.get('food_ids')
            if food_ids is None:
                return Response({"error": "Missing food_ids query parameter"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                [int(id) for id in food_ids.split(',')]
            except ValueError:
                return Response({"error": "Invalid food_ids query parameter. Must be a comma separated list of integers"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                user_y = float(self.request.query_params.get('y', self.default_location[0]))
                user_x = float(self.request.query_params.get('x', self.default_location[1]))
            except ValueError:
                return Response({"error": "Invalid y or x query parameter. Must be a float"}, status=status.HTTP_400_BAD_REQUEST)
            
            return super().list(request, *args, **kwargs)

#검색창
@api_view(['GET'])
def search_restaurants(request):
    search_query = request.GET.get('q')  # 검색
    
    if search_query:
        matching_restaurants = Restaurant.objects.filter(name__icontains=search_query)
        serialized_data = RestaurantBaseSerializer(matching_restaurants, many=True).data
        return Response(serialized_data)
    else:
        return Response([])
    

def koogle_cal(likes_cnt, review_cnt):
    if review_cnt <= 0 or likes_cnt <= 0: return 1

    avg_likes_per_review = likes_cnt / review_cnt

    if avg_likes_per_review >= 3: return 3
    if avg_likes_per_review >= 1.5: return 2

    return 1

class RestaurantView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailedInfoSerializer

    default_location = (37.5508, 126.9255)
    
    def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'request': self.request,
                'user_y' : float(self.request.query_params.get('y', self.default_location[0])),
                'user_x' : float(self.request.query_params.get('x', self.default_location[1])),
            }

    def get(self, request, *args, **kwargs):
        try: 
            float(self.request.query_params.get('y', self.default_location[0]))
            float(self.request.query_params.get('x', self.default_location[1]))
        except ValueError: 
            raise ValidationError('y and x query parameters must be a float')

        return super().get(request, *args, **kwargs)
