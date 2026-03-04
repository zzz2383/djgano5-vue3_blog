# 从 Django REST Framework 导入序列化器基类
from rest_framework import serializers
# 从当前目录的 models.py 导入文章模型
from .models import ArticlePost
# 从 users 应用的序列化器模块导入用户序列化器
from users.serializers import UserSerializer


class ArticlePostSerializer(serializers.ModelSerializer):
    """
    文章详情序列化器

    用于文章的**读取/展示**操作。包含所有字段，包括嵌套的作者详情。
    通常用于 GET 请求响应（如查看文章详情、列表）。
    """

    # 覆盖默认的外键字段 author，使用 UserSerializer 来序列化作者对象
    # read_only=True 表示此字段在创建/更新时不会被修改，仅用于输出
    author = UserSerializer(read_only=True)

    class Meta:
        # 指定此序列化器关联的模型
        model = ArticlePost
        # 指定序列化器输出的字段列表
        fields = [
            'id',  # 文章唯一标识
            'title',  # 文章标题
            'slug',  # URL友好标识（用于生成文章链接）
            'content',  # 文章正文内容
            'excerpt',  # 文章摘要/简介
            'author',  # 文章作者（被 UserSerializer 序列化）
            'created_at',  # 创建时间
            'updated_at',  # 最后更新时间
            'is_published',  # 是否发布状态
            'cover_image'  # 封面图片
        ]
        # 指定只读字段列表（这些字段不可通过API修改）
        read_only_fields = [
            'slug',  # 通常自动生成，不直接写入
            'created_at',  # 创建时间由系统自动设置
            'updated_at',  # 更新时间由系统自动设置
            'author'  # 作者从当前登录用户获取，不通过API指定
        ]


class ArticlePostCreateSerializer(serializers.ModelSerializer):
    """
    文章创建序列化器

    专门用于文章的**创建**操作。字段经过精简，避免暴露不必要的字段。
    通常用于 POST 请求（创建新文章）。
    """

    class Meta:
        # 指定此序列化器关联的模型
        model = ArticlePost
        # 仅包含创建文章时用户可指定的字段
        fields = [
            'title',  # 文章标题（必填）
            'content',  # 文章正文（必填）
            'excerpt',  # 文章摘要（选填）
            'cover_image',  # 封面图片（选填）
            'is_published'  # 是否发布（选填，通常默认不发布）
        ]
        # 字段级别的额外参数配置
        extra_kwargs = {
            'cover_image': {
                'required': False,  # 该字段不是必填项
                'allow_null': True  # 允许该字段值为 null（数据库为空）
            },
            'excerpt': {
                'required': False,  # 该字段不是必填项
                'allow_blank': True  # 允许该字段为空字符串（与 allow_null 不同）
            },
            'is_published': {
                'required': False,  # 该字段不是必填项
                'default': False  # 如果不提供，默认为 False（草稿状态）
            }
        }

    # 注意：这里不需要定义 read_only_fields
    # 因为所有字段都已明确指定，且没有包含 slug、created_at 等自动生成字段