from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    自定义用户模型
    继承自Django内置的AbstractUser基类
    """

    # ========== 字段定义 ==========

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # 添加自定义邮箱字段（必须唯一）
    email = models.EmailField(
        unique=True,  # 邮箱唯一
    )

    # 个人简介（可选字段）
    bio = models.TextField(
        blank=True,  # 允许为空
    )

    # 头像字段（可选）
    avatar = models.ImageField(
        upload_to='avatars/',  # 上传到avatars目录
        blank=True,  # 允许为空
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 修改时间

    # ========== 方法定义 ==========

    def __str__(self):
        """
        定义对象的字符串表示
        用于admin界面和shell显示
        """
        return self.username  # 返回用户名作为标识
