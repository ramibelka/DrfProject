from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from profiles.models import UserProfile, UserRating
from profiles.serializers import ProfileSerializer, UserRatingSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

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

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        obj.articles.all()  # Prefetch related articles
        obj.profile_user.followers.all()  # Prefetch related followers
        obj.profile_user.following.all()  # Prefetch related followings
        return obj

#####################################
## profile de l'utilisateur current 
class CurrentProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.userprofile

#####################################
class UserRatingCreateView(generics.CreateAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        rated_user = self.get_rated_user()
        serializer.save(rater=self.request.user, rated_user=rated_user)

    def get_rated_user(self):
        rated_user = self.serializer.validated_data.get('rated_user')
        if not rated_user:
            raise serializers.ValidationError("The 'rated_user' field is required.")
        return rated_user

class UserRatingListView(generics.ListAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return UserRating.objects.filter(rated_user_id=user_id)

##############################################################"
# abonne

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
############################################################################################
#evaluation

class UserRatingCreateView(generics.CreateAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserRating.objects.all()
    
    def perform_create(self, serializer):
        rated_user = self.get_rated_user()
        if rated_user is not None:
            rater = self.request.user
            # Check if the rater has already rated the rated_user
            if UserRating.objects.filter(rater=rater, rated_user=rated_user).exists():
                raise serializers.ValidationError("You have already rated this user.")
            serializer.save(rated_user=rated_user)

    def get_rated_user(self):
        username = self.request.data.get('rated_user')
        rated_user = get_object_or_404(User, username=username)
        return rated_user

    def get_object(self):
        # Override the get_object method to allow updating and removing ratings
        queryset = self.get_queryset()
        filter_kwargs = {'rater': self.request.user.id, 'rated_user': self.get_rated_user().id}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#additional permission for the reading 
class IsRatedUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET request for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow the rated user to modify the object
        return obj.rated_user == request.user

class UserRatingListView(generics.ListAPIView):
    serializer_class = UserRatingSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return UserRating.objects.filter(rated_user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_ratings = queryset.count()
        average_rating = queryset.aggregate(Avg('rating'))['rating__avg']
        
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'total_ratings': total_ratings,
            'average_rating': average_rating,
            'ratings': serializer.data
        }
        return Response(data)

#######################################################################################################

# class FollowerListView(generics.ListAPIView):
#     serializer_class = ProfileSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['pk']
#         user_profile = get_object_or_404(UserProfile, profile_user_id=user_id)
#         return user_profile.followers.all()

#     def get_permissions(self):
#         if self.request.user.is_authenticated:
#             # Allow only authenticated users to access the list
#             self.permission_classes = [permissions.IsAuthenticated]
#         else:
#             # Allow any user to access the count
#             self.permission_classes = [permissions.AllowAny]
#         return super().get_permissions()
