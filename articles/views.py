from rest_framework import generics, permissions , status
from .models import Article , Favoris, Comment, Like, Notification
from .serializers import ArticleSerializer , FavoriteSerializer,CommentSerializer, LikeSerializer, NotificationSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ArticleFilter
from django.db.models import Count


#pour Afficher la liste des articles  : GET
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#pour ajouter un articles :POST
class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

#pour recuperer un article (afficher un article ) : GET
class ArticleRetrieveView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []

#1 ajouter des condition de permission et que l'auteur de l'article est le seule qui peut acceder a ces fonctionnalité
class IsArticleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the owner of the article
        return obj.auteur == request.user

#pour modifier ou supprimer un article : PUT , DELETE
class ArticleUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated,IsArticleOwner]

############################################################
# # # class CategoryArticlesView(generics.RetrieveAPIView):
# # #     serializer_class = ArticleSerializer
# # #     permission_classes = [permissions.AllowAny]

# # #     def get(self, request):
# # #         categories = Article.objects.values_list('categorie', flat=True).distinct()  # Retrieve all unique categories
# # #         categorized_articles = {}  # Dictionary to store categorized articles

# # #         for category in categories:
# # #             articles = Article.objects.filter(categorie=category)  # Get articles for each category
# # #             serialized_articles = self.serializer_class(articles, many=True)  # Serialize articles
# # #             categorized_articles[category] = serialized_articles.data  # Store serialized articles in the dictionary

# # #         return Response(categorized_articles)

#recuperer list des article de chaque categorie  : GET
#pour les hommes
class MenArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(categorie='Men')
#pour les femmes
class WomenArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(categorie='Women')

#pour les enfants

class KidsArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(categorie='Kids')

#pour categorie sport
class SportsArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Article.objects.filter(categorie='Sport')

########################################################
#ajout d'un commentaire : POST

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


###comments and likes
#permission class
class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user is the owner of the comment
        return obj.user == request.user

#delete a comment : DELETE
class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated ,IsCommentOwner]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(user=user)

#affichage d'un list de commentaire : GET
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]

    def get_queryset(self):
        article_id = self.kwargs['pk']
        return Comment.objects.filter(article_id=article_id)

#majout et suppression ta3 like
class LikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # récupérer les détails d'un article 3la hssab l id.
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # récupérer l'objetArticle correspondant à cet ID, puis sérialiser les données de l'article
    def get_object(self):
        article_id = self.kwargs['pk']
        return Article.objects.get(pk=article_id)

    #add or Delete a like selon l'existance de l'inexistance de de jaime
    def post(self, request, *args, **kwargs):
        article = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, article=article)
        if not created:
            like.delete()
            message = 'Like removed.'
        else:
            message = 'Like added.'
        serializer = self.get_serializer(article)
        return Response({'article': serializer.data, 'message': message}, status=status.HTTP_200_OK)

##############################################################################""
#notifications view : GET list mratbin men akhir dat ll louel 
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated,IsArticleOwner]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-date_et_heure')

###########################################################################################"
#favoris :
#ajouter article au favoris

class FavoriteCreateView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

#créer ou supprimer un article des favoris. 
    def create(self, request, *args, **kwargs):
        #L'ID de l'article (pk) est récupéré à partir des paramètres de la requête (kwargs).
        article_id = kwargs.get('pk')
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        favorite_exists = Favoris.objects.filter(user=request.user, article=article).exists()

        if favorite_exists:
            # Remove the article from favorites
            Favoris.objects.filter(user=request.user, article=article).delete()
            return Response({'message': 'Article removed from favorites'}, status=status.HTTP_200_OK)
        else:
            # Add the article to favorites
            favorite = Favoris(user=request.user, article=article)
            favorite.save()
            serializer = self.get_serializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

#afficher Liste des favoris /GET
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favoris.objects.filter(user=self.request.user)

 ###############################################################################
 #filtrage et rechercher 
class ArticleSearchListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ArticleFilter #filter formulaire  filter.py li lfo9 fih les attrkbutes li 3la assashem derna filtre 
    search_fields = ['nom_article', 'description']
    pagination_class = None
    permission_classes = []