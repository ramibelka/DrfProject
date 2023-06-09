from rest_framework import serializers
from profiles.models import UserProfile
from articles.models import Article
from django.contrib.auth import get_user_model
from authentication.serializers import UserSerializer


User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['nom_article', 'prix', 'description', 'categorie', 'disponibilite', 'photo', 'Etat', 'taille', 'Date_cr']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile_user.username', read_only=True)
    photo_de_profile = serializers.ImageField(source='profile_user.photo_de_profile', read_only=True)
    description = serializers.CharField(source='profile_user.description',read_only=True )
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    articles = serializers.SerializerMethodField(read_only=True)

    def get_followers(self, obj):
        followers = obj.profile_user.followers.all()
        return UserSerializer(followers, many=True).data

    def get_following(self, obj):
        following = obj.profile_user.following.all()
        return UserSerializer(following, many=True).data

    # def get_articles(self, obj):
    
    #     articles = obj.articles.all()
    #     return ArticleSerializer(articles, many=True).data
    def get_articles(self, obj):
        articles = obj.articles.all()
        article_data = []
        for article in articles:
            serialized_article = ArticleSerializer(article).data
            article_data.append(serialized_article)
        return article_data


    class Meta:
        model = UserProfile
        fields = ['username', 'photo_de_profile', 'description', 'followers', 'following', 'articles']
