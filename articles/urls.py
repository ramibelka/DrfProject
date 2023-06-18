from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='liste-des-articles'),
    path('articles/ajouter/', views.ArticleCreateView.as_view(), name='ajouter-article'),
    path('articles/<int:pk>/', views.ArticleRetrieveView.as_view(), name='afficher-article'),
    path('articles/<int:pk>/modifer/', views.ArticleUpdateDestroyView.as_view(), name='modifer-article'),
    path('articles/<int:pk>/supprimer/', views.ArticleUpdateDestroyView.as_view(), name='Supprimer-article'),
#favoris urls 
    path('articles/<int:pk>/ajouter-aux-favoris/', views.FavoriteCreateView.as_view(), name='ajouter-aux-favoris'),
    path('list-des-favoris/', views.FavoriteListView.as_view(), name='list-des-favoris'),
#search and filters 
    path('articles/search-filter/', views.ArticleSearchListAPIView.as_view(), name='article-search'),

    path('articles/<int:pk>/comments/ajouter', views.CommentCreateView.as_view(), name='comment-create'),
    path('articles/comments/<int:pk>/delete', views.CommentDestroyView.as_view(), name='comment-destroy'),
    path('articles/<int:pk>/like/', views.LikeView.as_view(), name='like'),

]
