from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class ProfileCreationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create_user_profile(self, user):
        UserProfile.objects.get_or_create(profile_user=user)  # Set other attributes as needed

    def post(self, request):
        user = request.user
        self.create_user_profile(user)
        return Response({'message': 'User profile created successfully'}, status=status.HTTP_201_CREATED)

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.get_or_create(profile_user=instance)  # Set other attributes as needed

class FollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)
        user_profile = UserProfile.objects.get(profile_user=request.user)
        if user_profile.following.filter(pk=pk).exists():
            return Response({'message': 'User is already followed'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile.following.add(user_to_follow)
        return Response({'message': 'User followed successfully'}, status=status.HTTP_200_OK)

class UnfollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, pk):
        user_to_unfollow = get_object_or_404(User, pk=pk)
        user_profile = UserProfile.objects.get(profile_user=request.user)
        if not user_profile.following.filter(pk=pk).exists():
            return Response({'message': 'User is already unfollowed'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile.following.remove(user_to_unfollow)
        return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_200_OK)
