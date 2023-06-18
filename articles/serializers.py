from rest_framework import serializers
from .models import Article ,Favoris , Comment, Like

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'comment', 'created_at']

class ArticleSerializer(serializers.ModelSerializer):
    auteur = serializers.ReadOnlyField(source='auteur.username')
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    photo_de_profile = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id',
            'auteur',
            'nom_article',
            'photo_de_profile',
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
        read_only_fields = ['id','likes']

    def get_like_count(self, instance):
        return instance.likes.count()

    def get_is_liked(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return instance.likes.filter(id=user.id).exists()
        return False
#tp display the profile picture of the user in the article section 
    def get_photo_de_profile(self, instance):
        return instance.auteur.photo_de_profile.url if instance.auteur.photo_de_profile else None

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favoris
        fields = ['id', 'user', 'article']
        read_only_fields = ['id', 'user', 'article']

