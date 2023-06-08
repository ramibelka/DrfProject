from django.urls import path
from .views import ArticleListView, ArticleCreateView, ArticleRetrieveView, ArticleUpdateDestroyView ,FavoriteCreateView, FavoriteListView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='liste-des-articles'),
    path('articles/ajouter/', ArticleCreateView.as_view(), name='ajouter-article'),
    path('articles/<int:pk>/', ArticleRetrieveView.as_view(), name='afficher-article'),
    path('articles/<int:pk>/modifer/', ArticleUpdateDestroyView.as_view(), name='modifer-article'),
    path('articles/<int:pk>/supprimer/', ArticleUpdateDestroyView.as_view(), name='Supprimer-article'),
#favoris urls 
    path('articles/<int:pk>/ajouter-aux-favoris/', FavoriteCreateView.as_view(), name='ajouter-aux-favoris'),
    path('list-des-favoris/', FavoriteListView.as_view(), name='list-des-favoris'),

]

