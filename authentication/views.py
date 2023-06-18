from rest_framework import generics, permissions ,status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission


#we defined this class to ad it to list of permissions cuz only unauthentifacted peaple who can reach teh sign up view and page 
class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

User = get_user_model()
#inscription

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, _ = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'token': token.key, 'user_id': user.id},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()


#authtentifier
class LoginView(ObtainAuthToken):
    http_method_names = ['post', 'get']
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handle the POST request to obtain the token
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user) 
        return Response({'token': token.key, 'user_id': user.id})

    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Login GET method not supported. Please use the POST method to login.'})


#deconnecter 
class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({'detail': 'Successfully logged out.'})
