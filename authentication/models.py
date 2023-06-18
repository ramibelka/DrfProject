# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# from profiles.models import UserProfile

class User(AbstractUser):

    username = models.CharField(max_length=30, blank=False, null=False, unique=True)
    nom = models.CharField(max_length=30, blank=False, null=True)
    prenom = models.CharField(max_length=30, blank=False, null=True)
    date_de_naissance = models.DateField(null=True )
    adr_email = models.EmailField( blank=False, null=True)
    password = models.CharField(max_length=100, blank=False, null=True)
    localisation = models.CharField(max_length=100, null=True)
    numero_de_tel = PhoneNumberField(max_length=13,null=True)
    description = models.TextField(null=True)
    photo_de_profile = models.ImageField(upload_to='profile/', null=True)
    
#relation avec userprofile table 
   # user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
         return self.username
    


