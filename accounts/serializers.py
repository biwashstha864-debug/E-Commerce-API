from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
        ]
        
        extra_kwargs = {
            "password" : {
                "write_only" : True
            }
        }
        
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_password(self,value):
        validate_password(value)
        return value