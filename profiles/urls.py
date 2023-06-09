from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/abonner/', views.FollowView.as_view(), name='profile-follow'),
    path('profiles/<int:pk>/desabonner/', views.UnfollowView.as_view(), name='profile-unfollow'),

]