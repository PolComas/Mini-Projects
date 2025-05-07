from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .models import Tweet, UserProfile
from .serializers import TweetSerializer, UserRegisterSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserTweetsList(generics.ListAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Tweet.objects.filter(author__id=user_id).order_by('-created_at')

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            request.user.profile.following.add(user_to_follow.profile)
            return Response({'detail': f"Now following {user_to_follow.username}"})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            request.user.profile.following.remove(user_to_unfollow.profile)
            return Response({'detail': f"Unfollowed {user_to_unfollow.username}"})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ListFollowingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return self.request.user.profile.following.all()

class ListFollowersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return self.request.user.profile.followers.all()

class TimelineView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        following_users = self.request.user.profile.following.values_list('user', flat=True)
        return Tweet.objects.filter(author__id__in=following_users).order_by('-created_at')
