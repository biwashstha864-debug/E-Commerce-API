from rest_framework import generics
from .models import User
from .serializers import RegisterSerailizer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerailizer
    
class LoginView(TokenObtainPairView):
    pass
