from rest_framework import serializers
from .models import Article ,Favoris 

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'nom_article',
            'prix',
            'description',
            'categorie',
            'disponibilite',
            'photo',
            'Etat',
        ]
        read_only_fields = ['id']

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favoris
        fields = ['id', 'user', 'article']
        read_only_fields = ['id', 'user', 'article']

