# 导入Django的核心路由模块
from django.urls import path, include
# 导入DRF的默认路由器（自动生成标准REST路由）
from rest_framework.routers import DefaultRouter
# 导入自定义的视图集和视图
from .views import ArticlePostViewSet

# 1. 创建DRF默认路由器实例
# DefaultRouter会自动生成标准的RESTful风格URL
router = DefaultRouter()

# 2. 注册视图集到路由器
# 'articles' - URL前缀
# ArticlePostViewSet - 关联的视图集类
# basename='article' - 用于URL反向解析的基础名称
router.register(r'articles', ArticlePostViewSet, basename='article')

# 调试输出：打印自动生成的路由模式

# 3. 定义项目的URL模式列表
urlpatterns = [
    # 包含路由器生成的所有路由，前缀为'api/articles/'
    # 例如：
    # - /api/articles/          - 列表和创建
    # - /api/articles/{id}/     - 详情、更新、删除
    path('', include(router.urls)),
]
