from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 获取当前激活的用户模型
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    用于用户信息的序列化和反序列化
    """
    avatar = serializers.SerializerMethodField()  # 自定义头像字段处理

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'is_active', 'bio']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_avatar(self, obj):
        """返回完整的头像URL"""
        if obj.avatar:
            # 构建完整的URL
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return f"{settings.BASE_URL}{obj.avatar.url}"
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器
    仅返回 id, username, avatar, bio 字段
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'bio']  # 只暴露这些字段
        read_only_fields = ['id', 'username']  # id和username不可通过API修改

    def get_avatar(self, obj):
        """返回完整的头像URL"""
        if obj.avatar:
            # 构建完整的URL
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return f"{settings.BASE_URL}{obj.avatar.url}"
        return None


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    处理用户注册数据的验证和用户创建
    """

    # 邮箱字段配置
    email = serializers.EmailField(
        required=True,  # 必填字段
        validators=[  # 验证器列表
            UniqueValidator(  # 唯一性验证
                queryset=User.objects.all(),  # 验证所有用户邮箱唯一
                message="该邮箱已被注册"  # 自定义错误消息（可选）
            )
        ]
    )

    # 密码字段配置
    password = serializers.CharField(
        write_only=True,  # 只用于输入，不包含在序列化输出中
        required=True,  # 必填字段
        style={'input_type': 'password'}  # 在可浏览API中显示为密码输入框
    )

    class Meta:
        model = User  # 关联的用户模型
        fields = ('username', 'email', 'password')  # 包含的字段

        # 可选：字段级别的额外验证选项
        extra_kwargs = {
            'username': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="用户名已被占用"
                    )
                ]
            }
        }

    def create(self, validated_data):
        """
        创建用户实例
        :param validated_data: 已验证的数据
        :return: 新创建的用户实例
        """
        # 使用Django的create_user方法创建用户
        # 该方法会自动处理密码哈希
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  # 密码会自动加密
        )

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT令牌序列化器
    扩展标准的JWT令牌返回数据
    """

    def validate(self, attrs):
        """
        验证方法 - 添加自定义返回数据
        :param attrs: 属性字典
        :return: 包含令牌和用户信息的数据字典
        """
        # 调用父类方法获取基础令牌数据
        data = super().validate(attrs)

        # 添加用户信息到返回数据中
        data['user'] = UserSerializer(self.user).data

        return data
