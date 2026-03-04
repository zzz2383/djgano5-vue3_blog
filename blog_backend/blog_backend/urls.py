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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ↑ 开发环境媒体文件服务配置 ↑
#
# static() 函数的作用：
# 1. 第一个参数 settings.MEDIA_URL：
#    - 通常配置为 '/media/'，表示媒体文件的访问路径前缀
#    - 对应 settings.py 中的 MEDIA_URL 配置
#
# 2. 第二个参数 document_root=settings.MEDIA_ROOT：
#    - 指定媒体文件在服务器上的实际存储路径
#    - 对应 settings.py 中的 MEDIA_ROOT 配置
