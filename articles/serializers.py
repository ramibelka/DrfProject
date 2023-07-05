from requests import request
from rest_framework import serializers
from .models import Article ,Favoris , Comment, Like, Notification


#serializers ta3 like 
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

#serializers ta3 comentaire 
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'comment', 'created_at']

#serializers ta3 article
class ArticleSerializer(serializers.ModelSerializer):
    auteur_id = serializers.ReadOnlyField(source='auteur.id')
    auteur = serializers.ReadOnlyField(source='auteur.username')
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_saved = serializers.SerializerMethodField(read_only=True)
    photo_de_profile = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ['id',
            'auteur_id',
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
            'is_liked',
            'is_saved']
        read_only_fields = ['id','likes','auteur_id', 'Date_cr']

    def get_like_count(self, instance):
        return instance.likes.count()

    def get_is_liked(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return instance.likes.filter(user=user).exists()
        return False

#pour afficher status ou l'article ida rahou saved or not        
    def get_is_saved(self, instance):  
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return instance.favoris.filter(user=user).exists()
        return False
#afficher phtoto de profile ta3 luser f wast article bah yekhdem biha fl frontend 
    def get_photo_de_profile(self, instance):
        request = self.context.get('request')
        if instance.auteur.photo_de_profile and request:
            return request.build_absolute_uri(instance.auteur.photo_de_profile.url)
        else:
            return None
        
#favoris serializers 
class FavoriteSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    class Meta:
        model = Favoris
        fields = ['article']

#notification serializer 
class NotificationSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'article_id', 'contenu', 'date_et_heure', 'etat']

    def get_article_id(self, obj):
        return obj.article.id if obj.article else None