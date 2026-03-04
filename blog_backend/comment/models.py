from django.db import models

from articles.models import ArticlePost
from users.models import User


# Create your models here.
class Comment(models.Model):
    """
    文章评论模型
    """
    # 评论内容
    content = models.TextField()

    # 评论作者，外键关联到用户模型
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 关联的文章，外键关联到文章模型
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')

    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)

    # 是否活跃（可用于软删除）
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.author.username} 对 {self.article.title} 的评论"