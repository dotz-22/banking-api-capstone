from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class NewUser(AbstractUser):
        
        ROLE =(('customer', 'Customer'),
               ('admin', 'Admin')
               )
    
        username = None
        first_name= models.CharField(max_length=250)
        last_name= models.CharField(max_length=250)
        email = models.EmailField(unique=True)
        phone_number= models.CharField(max_length=11, null=True, unique=True, blank=True)
        role = models.CharField(max_length=40, choices=ROLE, blank=True, null=True, default='customer')

        
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        objects = CustomUserManager()
    
        def __str__(self):
         return self.email
