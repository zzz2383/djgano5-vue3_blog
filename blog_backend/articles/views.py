# 导入DRF核心模块
from rest_framework import viewsets, permissions
# 导入当前应用的模型
from .models import ArticlePost
# 导入当前应用的序列化器
from .serializers import ArticlePostSerializer, ArticlePostCreateSerializer


class ArticlePostViewSet(viewsets.ModelViewSet):
    """
    博客文章视图集
    提供完整的CRUD (Create, Retrieve, Update, Delete) API端点

    实际API端点：
    - 列表查看：GET /api/articles/
    - 创建文章：POST /api/articles/
    - 获取详情：GET /api/articles/{id}/
    - 更新文章：PUT /api/articles/{id}/
    - 部分更新：PATCH /api/articles/{id}/
    - 删除文章：DELETE /api/articles/{id}/
    """

    # 定义默认查询集（获取所有博客文章，按创建时间降序排列）
    queryset = ArticlePost.objects.all().order_by('-created_at')

    # 指定默认使用的序列化器类（用于展示）
    serializer_class = ArticlePostSerializer

    # 设置权限控制：
    # IsAuthenticatedOrReadOnly - 认证用户可写，匿名用户只读
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        重写创建方法
        在创建新博客文章时自动关联当前用户作为作者

        参数:
            serializer: 已验证的序列化器实例
        """
        serializer.save(author=self.request.user)  # 自动设置作者为当前用户

    def get_serializer_class(self):
        """
        动态选择序列化器
        根据请求方法返回不同的序列化器类
        """
        if self.action == 'create':
            return ArticlePostCreateSerializer  # 创建时使用专用序列化器
        return super().get_serializer_class()  # 其他情况使用默认序列化器


