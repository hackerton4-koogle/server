from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.conf import settings
import jwt
from django.shortcuts import render

from .models import User
from .models import Country
from django.contrib.sessions.backends.db import SessionStore

class CountriesListView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        return render(request, 'signup_form.html', {'countries': countries})
        # countries = Country.objects.all().values_list('name', flat=True)
        # return Response(countries)
    
class SignupView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        context = {'countries': countries}
        return render(request, 'signup_form.html', context)
    
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        country = request.data.get('country')

        hashed_password = make_password(password)
        user = User.objects.create(name=name, password=hashed_password, country=country)
        
        payload = {'user_id': user.id, 'name': user.name, 'country': user.country} # type: ignore
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        # 회원가입이 완료되었다는 문구와 메인페이지로 가기 버튼을 포함한 페이지 렌더링
        context = {'name': name}
        return render(request, 'signup_complete.html', context)

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')

        user = authenticate(request, username=name, password=password)
        if user:
            payload = {'user_id': user.id, 'name': user.name, 'country': user.country} # type: ignore
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        else:
            return Response({'message': 'Login failed.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        # 로그아웃은 클라이언트 측에서 JWT를 삭제하면 됩니다.
        logout(request)
        return Response({'message': 'Logged out.'})
