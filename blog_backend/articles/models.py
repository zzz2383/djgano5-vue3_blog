from django.db import models
from users.models import User  # 导入自定义用户模型
from django.utils.text import slugify  # 导入slugify工具函数


class ArticlePost(models.Model):
    """
    博客文章模型
    定义了博客文章的数据结构和相关方法
    """

    # 文章标题，CharField类型，最大长度200字符
    title = models.CharField(max_length=200)

    # 文章slug(用于URL)，SlugField类型，自动生成，唯一且可为空
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # 文章内容，TextField类型，不限长度
    content = models.TextField()

    # 文章摘要，CharField类型，最大长度300字符，可为空
    excerpt = models.CharField(max_length=300, blank=True)

    # 文章作者，外键关联到User模型，级联删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 创建时间，DateTimeField类型，自动设置为对象首次创建时的时间
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新时间，DateTimeField类型，每次保存对象时自动更新
    updated_at = models.DateTimeField(auto_now=True)

    # 发布状态，BooleanField类型，默认未发布
    is_published = models.BooleanField(default=False)

    # 封面图片，ImageField类型，上传到article_covers/目录，可为空
    cover_image = models.ImageField(upload_to='article_covers/', null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        重写save方法，在保存前自动生成slug
        如果slug为空，则使用标题生成slug
        """
        if not self.slug:
            self.slug = slugify(self.title)  # 使用slugify将标题转换为URL友好的格式
        super().save(*args, **kwargs)  # 调用父类的save方法完成保存

    def __str__(self):
        """
        定义对象的字符串表示形式
        在管理后台和其他需要显示对象的地方使用
        """
        return self.title  # 返回文章标题作为对象的字符串表示

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

