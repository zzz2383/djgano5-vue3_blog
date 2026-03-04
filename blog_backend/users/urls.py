from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# 从当前目录的views模块导入视图类
from .views import (
    UserRegisterView,  # 用户注册视图
    CustomTokenObtainPairView,  # 自定义Token获取视图
    UserProfileView,  # 用户个人资料视图
    LogoutView,         # 用户退出·登录·视图
)

urlpatterns = [
    # 用户注册接口
    path('user/register/', UserRegisterView.as_view(), name='register'),
    # 用户登录接口
    path('user/login/', CustomTokenObtainPairView.as_view(), name='login'),

    path('user/logout/', LogoutView.as_view(), name='logout'),
    # 用户个人资料接口
    path('user/profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    # 刷新口令
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
