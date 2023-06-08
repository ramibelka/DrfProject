from .forms import ArticleForm
from rest_framework import generics, permissions , status
from .models import Article , Favoris
from .serializers import ArticleSerializer , FavoriteSerializer
from rest_framework.response import Response

#pour Afficher la liste des articles 
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#pour Creer un articles 
class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

#pour recuperer un article (afficher un article )
class ArticleRetrieveView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#1 ajouter des condition de permission et que l'auteur de l'article est le seule qui peut acceder a ces fonctionnalité 
class IsArticleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the owner of the article
        return obj.auteur == request.user
    
#pour modifier ou supprimer un article 
class ArticleUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,IsArticleOwner]

###########################################################################################"
#favoris :

#ajouter article au favoris 
class FavoriteCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favoris.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        article_id = request.data.get('article_id')
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
        
        favorite, created = Favoris.objects.get_or_create(user=request.user, article=article)
        
        if created:
            serializer = self.get_serializer(favorite)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'Article already added to favorites'}, status=status.HTTP_400_BAD_REQUEST)


# afficher favorite list
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favoris.objects.filter(user=self.request.user)
