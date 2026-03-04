# 导入DRF核心模块
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

# 导入当前应用的模型
from .models import Comment
# 导入当前应用的序列化器
from .serializers import CommentSerializer
# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    支持标准的CRUD操作和自定义操作
    """
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        重写get_queryset方法，支持按文章ID过滤评论
        """
        queryset = super().get_queryset()
        article_id = self.request.query_params.get('article_id')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        print(queryset)
        return queryset

    def perform_create(self, serializer):
        """
        创建评论时自动设置作者
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        点赞评论的自定义动作
        """
        comment = self.get_object()
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            comment.likes.add(user)
            return Response({'status': 'liked'})

    def destroy(self, request, *args, **kwargs):
        """
        重写删除方法，实现软删除
        """
        instance = self.get_object()
        if instance.author != request.user and not request.user.is_staff:
            return Response(
                {'detail': '您没有权限删除此评论'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)