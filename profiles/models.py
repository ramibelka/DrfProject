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

    username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.profile_user.username
    
    #sauvegarder la valeur de username avec la valeur de username de user 
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.profile_user.username
        super().save(*args, **kwargs)


class UserRating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluateur',null=True)
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluated',null=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)],null=True)

    total_ratings = models.PositiveIntegerField(default=0)
    average_ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.rater} : {self.rating}-> {self.rated_user}: {self.rating} (Total Ratings: {self.total_ratings}, Average Rating: {self.average_rating})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_ratings_statistics()

    def update_ratings_statistics(self):
        ratings = UserRating.objects.filter(rated_user=self.rated_user)
        self.total_ratings = ratings.count()
        self.average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        self.rated_user.save()

