from django.urls import path
from profiles import views

urlpatterns = [
    path('profile/current/', views.CurrentProfileView.as_view(), name='current-profile'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/abonner/', views.FollowView.as_view(), name='profile-follow'),
    path('profiles/<int:pk>/desabonner/', views.UnfollowView.as_view(), name='profile-unfollow'),

    #path('profiles/<int:pk>/list-des-abonner/', views.FollowListView.as_view(), name='followings-list'),
    #path('profiles/<int:pk>/list-des-abonnement/', views.FollowerListView.as_view(), name='followers-list'),

    path('evaluation/ajouter/', views.UserRatingCreateView.as_view(), name='rating-create'),
    path('evaluation/', views.UserRatingListView.as_view(), name='rating-list'),
    
]