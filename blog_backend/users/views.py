from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# 导入自定义序列化器
from users.serializers import UserRegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer, \
    UserProfileSerializer

# 获取当前激活的用户模型
User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    """
    用户注册API视图
    继承自CreateAPIView提供标准的创建操作
    """

    queryset = User.objects.all()  # 关联的用户查询集
    serializer_class = UserRegisterSerializer  # 使用的注册序列化器
    permission_classes = [permissions.AllowAny]  # 允许任何人访问（无需认证）

    def post(self, request, *args, **kwargs):
        """
        处理POST注册请求
        重写父类方法以自定义响应格式
        """
        # 1. 获取并验证序列化器数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 验证失败自动返回400

        # 2. 保存用户数据（会调用序列化器的create方法）
        user = serializer.save()

        # 3. 返回自定义响应格式
        return Response({
            'user': UserSerializer(user).data,  # 用户基本信息
            'message': '用户注册成功！'  # 成功消息
        })


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义JWT认证视图
    使用自定义的序列化器扩展标准JWT响应
    """
    serializer_class = CustomTokenObtainPairSerializer  # 指定自定义序列化器


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    用户个人资料视图
    - 任何人可以查看用户信息 (GET)
    - 只有认证用户能修改自己的信息 (PUT/PATCH)
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 读操作无需认证，写操作需要认证

    def get_object(self):
        """
        获取用户对象
        - 对于GET请求：返回URL中指定的用户
        - 对于PUT/PATCH请求：确保只能修改自己的信息
        """
        if self.request.method in ['PUT', 'PATCH']:
            # 写操作时强制返回当前用户，确保只能修改自己
            return self.request.user
        else:
            # 读操作时返回URL参数指定的用户
            return super().get_object()

    def update(self, request, *args, **kwargs):
        """
        处理更新请求
        - 自动检查权限（通过permission_classes）
        - 确保用户只能修改自己的信息（通过get_object实现）
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=kwargs.pop('partial', False)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    """
    用户登出视图
    """

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except:
            return Response('退出错误')

