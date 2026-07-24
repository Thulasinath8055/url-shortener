from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    """
    POST /api/register/
    
    Public endpoint. Anyone can create an account.
    The serializer handles password hashing and email uniqueness validation.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]