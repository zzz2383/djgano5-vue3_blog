from rest_framework import serializers
from .models import ArticlePost
from users.serializers import UserSerializer


class ArticlePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ArticlePost
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'created_at', 'updated_at',
            'is_published', 'cover_image'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'author']


class ArticlePostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePost
        fields = ['title', 'content', 'excerpt', 'cover_image', 'is_published']
        extra_kwargs = {
            'cover_image': {'required': False, 'allow_null': True},
            'excerpt': {'required': False, 'allow_blank': True},
            'is_published': {'required': False, 'default': False}
        }
