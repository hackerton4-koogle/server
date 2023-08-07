from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .models import MyUser, Country
from django.contrib.sessions.backends.db import SessionStore

class CountriesListView(APIView):
    def get(self, request):
        countries = Country.objects.all().values_list('name', flat=True)
        return Response(countries)
    
class SignupView(APIView):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        country = request.data.get('country')

        hashed_password = make_password(password)
        user = MyUser.objects.create(name=name, password=hashed_password, country=country)
        
        payload = {'user_id': user.id, 'name': user.name, 'country': user.country} # type: ignore
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        context = {'name': name, 'country': country}
        return render(request, 'signup_complete.html', context)

class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')

        user = authenticate(request, username=name, password=password)
        if user:
            login(request, user) 
            return Response({'message': 'Logged in.'})
        else:
            return Response({'message': 'Login failed.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out.'})