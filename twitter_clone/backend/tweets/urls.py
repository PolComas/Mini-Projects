from django.urls import path, include
from rest_framework import routers
from .views import TweetViewSet, RegisterUserView, UserTweetsList
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'tweets', TweetViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='login'),
    path('api/users/<int:user_id>/tweets/', UserTweetsList.as_view(), name='user-tweets'),
]

from .views import FollowUserView, UnfollowUserView, ListFollowingView, ListFollowersView, TimelineView

urlpatterns += [
    path('api/follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('api/unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),
    path('api/following/', ListFollowingView.as_view(), name='following'),
    path('api/followers/', ListFollowersView.as_view(), name='followers'),
    path('api/timeline/', TimelineView.as_view(), name='timeline'),
]
