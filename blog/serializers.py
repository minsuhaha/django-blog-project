from rest_framework import serializers
from .models import Topic, Post, User, Content

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'