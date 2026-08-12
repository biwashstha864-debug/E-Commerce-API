from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN  = "ADMIN","Admin"
        CUSTOMER = "CUSTOMER","Customer"
         
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default = Role.CUSTOMER
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    
