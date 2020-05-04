from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from .serializers import UserSerializer, StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
 

# @api_view(['GET'])
# def get_user_view(request):
#     print(request.user)
#     data = {}
#     data['login'] = str(request.user)
#     # if request.user.is_authenticated():
#     #     return HttpResponse(json.dumps({
#     #         "is_authenticated": request.user.is_authenticated()
#     #         }), content_type='application/json')
#     return Response(data)

@api_view(['GET'])
def current_user(request):
    print(request.user)
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST'])
def login_view(request):
    data = request.data
    username, password = data.get('username'), data.get('password')
    user = authenticate(username=username, password=password)
    print(username, password)
    if user:
        login(request, user)
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def logout_view(request):
    print(request.data)
    logout(request)
    return Response(status=status.HTTP_200_OK)


