from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/foods', include('food.urls')),
    path('api/restaurants/', include('Restaurants.urls')),
    path('api/restaurants/reviews/', include('Reviews.urls')),
    path('api/user/', include('Users.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG == True:
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")), # django-debug-toolbar requirement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # to view media files