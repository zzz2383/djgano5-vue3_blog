from rest_framework import serializers
from articles.models import ArticlePost  # 导入ArticlePost模型
from .models import Comment
from users.serializers import UserSerializer  # 导入用户序列化器


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=ArticlePost.objects.all())

    class Meta:
        # 导入评论模型
        model = Comment
        # 需要序列化的内容：评论id、所属文章、评论内容、创建时间、更新时间
        fields = ['id', 'article', 'author', 'content', 'created_at', 'updated_at']
        # 只读字段
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        # 自动设置当前用户为评论作者
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
