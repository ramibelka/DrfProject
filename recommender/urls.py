from django.urls import path
from recommender import views


urlpatterns = [
    path('item/articles/<int:article_id>/item-similarity/', views.ItemSimilarityView.as_view(), name='item_similarity'),
]
