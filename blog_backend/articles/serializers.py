from rest_framework import serializers
from .models import ArticlePost  # 导入ArticlePost模型
from users.serializers import UserSerializer  # 导入用户序列化器


class ArticlePostSerializer(serializers.ModelSerializer):
    """
    博客文章详情序列化器
    用于文章详情的展示，包含完整的字段和嵌套的作者信息
    """

    # 覆盖默认的作者字段，使用UserSerializer来嵌套显示作者详情
    # read_only=True 表示此字段仅用于输出，不会被用于创建或更新
    author = UserSerializer(read_only=True)

    class Meta:
        model = ArticlePost  # 指定关联的模型
        fields = '__all__'  # 包含所有模型字段
        # 实际包含的字段：
        # - id, title, slug, content, excerpt
        # - author, created_at, updated_at
        # - is_published, cover_image


class ArticlePostCreateSerializer(serializers.ModelSerializer):
    """
    博客文章创建序列化器
    专门用于文章的创建操作，字段更精简且可控制
    """

    class Meta:
        model = ArticlePost
        # 只包含创建文章时真正需要的字段
        fields = ['title', 'slug', 'content', 'excerpt', 'cover_image']
        # 或者更精简：fields = ['title', 'content']

        extra_kwargs = {
            'slug': {'required': False},  # slug 可以自动生成
            'cover_image': {'required': False, 'allow_null': True},
            'excerpt': {'required': False, 'allow_blank': True}
        }

    def validate_slug(self, value):
        """验证slug，如果没有提供则自动生成"""
        from django.utils.text import slugify

        if not value and 'title' in self.initial_data:
            # 从标题生成slug
            value = slugify(self.initial_data['title'])

        return value
