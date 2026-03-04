from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet

# 创建默认路由器实例
# DefaultRouter 提供了标准的资源路由（list/create/retrieve/update/destroy）
router = DefaultRouter()

# 注册视图集到路由器
# r'comments' - 定义URL前缀为/comments/
# CommentViewSet - 关联的视图集类
# basename='comment' - 用于URL名称反转的基础名称
router.register(r'comments', CommentViewSet, basename='comment')

# URL配置列表
urlpatterns = [
    # 包含路由器生成的所有URL模式
    # 这将自动生成以下标准端点：
    # - /comments/ - GET: 列表 POST: 创建
    # - /comments/{pk}/ - GET: 详情 PUT/PATCH: 更新 DELETE: 删除
    path('', include(router.urls)),
]