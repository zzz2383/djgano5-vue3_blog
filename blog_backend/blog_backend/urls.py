"""
URL configuration for blog_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 导入必要的模块
from django.conf import settings  # 访问Django项目设置
from django.conf.urls.static import static  # 用于静态文件服务
from django.contrib import admin  # 管理后台模块
from django.urls import path, include  # URL路由工具

# 主URL配置列表
urlpatterns = [
    # Django自带的后台管理系统URL
    # 访问路径: http://<domain>/admin/
    path('admin/', admin.site.urls),

    # 包含其他应用的URL配置
    # 所有以/api/开头的请求会转发到users应用的urls.py处理
    # 例如: /api/user/ → 由users.urls处理
    path('api/', include('users.urls')),
]

# 作用：让Django开发服务器能够提供用户上传的媒体文件
urlpatterns += static(
    settings.MEDIA_URL,  # 媒体文件的URL前缀（如/media/）
    document_root=settings.MEDIA_ROOT  # 媒体文件的实际存储路径
)