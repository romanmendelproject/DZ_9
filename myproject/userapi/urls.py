from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import registration_view, login_view, logout_view, current_user

api_router = DefaultRouter()

urlpatterns = [
    #path('getuser', get_user_view, name='get_user'),
    path('register', registration_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('cur', current_user, name='current_user'),
    
]
urlpatterns += api_router.urls
