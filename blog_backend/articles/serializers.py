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
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = ArticlePost  # 指定关联的模型
        # 只包含创建文章时需要的字段
        fields = ['id', 'title', 'slug', 'content', 'excerpt',
                  'created_at', 'updated_at', 'is_published', 'cover_image',
                  'comment_count']

        # 额外的字段选项配置
        extra_kwargs = {
            # 封面图片不是必填字段，允许为null
            'cover_image': {
                'required': False,  # 非必填
                'allow_null': True  # 允许为null
            },
            # 摘要不是必填字段，允许为空字符串
            'excerpt': {
                'required': False,  # 非必填
                'allow_blank': True  # 允许空字符串
            }
        }

    def get_comment_count(self, obj):
        return obj.comments.filter(is_active=True).count()
