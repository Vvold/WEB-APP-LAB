from rest_framework import serializers
from .models import Task, BaseAppInfo, User, UserProfile


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']


class BaseAppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAppInfo
        fields = ['description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['email', 'gender', 'birth_date']
