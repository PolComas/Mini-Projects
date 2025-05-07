from rest_framework import serializers
from .models import Tweet, UserProfile
from django.contrib.auth.models import User

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = Tweet
        fields = ['id', 'text', 'created_at', 'author']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    following = serializers.StringRelatedField(many=True, read_only=True)
    followers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'following', 'followers']
