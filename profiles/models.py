from django.contrib.auth import get_user_model
from django.db import models
from authentication.models import User
from articles.models import Article

User = get_user_model()

class UserProfile(models.Model):

    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    articles = models.ManyToManyField(Article, related_name='Auteur', blank=True)

    def __str__(self):
        return self.profile_user.username
    
 