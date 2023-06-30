from rest_framework import serializers
from articles.serializers import CommentSerializer
from profiles.models import UserProfile, UserRating
from articles.models import Article
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
#evaluation serialiser

class UserRatingSerializer(serializers.ModelSerializer):
    rater = serializers.PrimaryKeyRelatedField(read_only=True, source='rater.username',default=serializers.CurrentUserDefault())
    rated_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    rating = serializers.IntegerField(min_value=1, max_value=5)

    total_ratings = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    
    def get_total_ratings(self, obj):
        ratings = UserRating.objects.filter(rated_user=obj.rated_user)
        total_ratings = ratings.count()
        return total_ratings
    
    def get_average_rating(self, obj):
        ratings = UserRating.objects.filter(rated_user=obj.rated_user)
        average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
        return average_rating

    def create(self, validated_data):
        rater = self.context['request'].user
        rated_user = validated_data.get('rated_user')
        rating = self.get_existing_rating(rater, rated_user)
        
        if rating:
            # Rating already exists, update it
            rating.rating = validated_data.get('rating')
            rating.save()
            return rating
        else:
            # Rating doesn't exist, create it
            return UserRating.objects.create(rater=rater, **validated_data)
        
    def get_existing_rating(self, rater, rated_user):
        ratings = UserRating.objects.filter(rater=rater, rated_user=rated_user).order_by('-id')
        if ratings.exists():
            return ratings.first()
        return None

    class Meta:
        model = UserRating
        fields = ['rater', 'rated_user', 'rating', 'total_ratings', 'average_rating']
        read_only_fields = ['rater']
        unique_together = ('rater', 'rated_user')


#article serializer
class ArticleSerializer(serializers.ModelSerializer):
    auteur_id = serializers.ReadOnlyField(source='auteur.id')
    auteur = serializers.ReadOnlyField(source='auteur.username')
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Article
        fields = ['id',
            'auteur_id',
            'auteur',
            'nom_article',
            'prix',
            'description',
            'categorie',
            'disponibilite',
            'photo',
            'Etat',
            'taille', 
            'Date_cr', 
            'likes', 
            'comments', 
            'like_count',
            'is_liked',]
        read_only_fields = ['id','likes','auteur_id', 'Date_cr']


    def get_like_count(self, instance):
        return instance.likes.count()

    def get_is_liked(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return instance.likes.filter(user=user).exists()
        return False

#profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile_user.username', read_only=True)
    photo_de_profile = serializers.ImageField(source='profile_user.photo_de_profile', read_only=True)
    description = serializers.CharField(source='profile_user.description',read_only=True )
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    articles = serializers.SerializerMethodField(read_only=True)

   # ratings_received = UserRatingSerializer(many=True, read_only=True)
    total_ratings = serializers.SerializerMethodField(read_only=True)
    raters_count = serializers.SerializerMethodField(read_only=True)
    
#tafficher list ta3l folowers w following ms b le nom ta3hem brk
    def get_followers(self, obj):
        followers = obj.profile_user.followers.all()
        follower_usernames = [follower.profile_user.username for follower in followers]
        return follower_usernames

    def get_following(self, obj):
        following = obj.profile_user.following.all()
        following_usernames = [follow.profile_user.username for follow in following]
        return following_usernames

    def get_articles(self, obj):
        articles = obj.profile_user.articles.all()
        article_data = []
        for article in articles:
            serialized_article = ArticleSerializer(article).data
            article_data.append(serialized_article)
        return article_data

    def get_total_ratings(self, obj):
        ratings = UserRating.objects.filter(rated_user=obj.profile_user)
        total_ratings = ratings.count()
        return total_ratings

    def get_raters_count(self, obj):
        raters = UserRating.objects.filter(rated_user=obj.profile_user).values('rater').distinct()
        raters_count = raters.count()
        return raters_count
    
    class Meta:
        model = UserProfile
        fields = [  'username',
                    'photo_de_profile', 
                    'description', 
                    'followers',
                    'following',
                    'articles',
                    'raters_count',
                    'total_ratings'
                ]
