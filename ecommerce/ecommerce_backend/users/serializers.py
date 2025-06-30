from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用戶註冊序列化器"""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'gender', 'dob'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """驗證密碼確認"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密碼與確認密碼不匹配")
        return attrs

    def validate_email(self, value):
        """驗證 email 唯一性"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("此 email 已被註冊")
        return value

    def create(self, validated_data):
        """創建新用戶"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """用戶登入序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """驗證用戶登入憑證"""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # 支援用戶名或 email 登入
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    raise serializers.ValidationError("無效的登入憑證")

            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("無效的登入憑證")

            if not user.is_active:
                raise serializers.ValidationError("用戶帳戶已被停用")

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("必須提供用戶名和密碼")


class UserProfileSerializer(serializers.ModelSerializer):
    """用戶資料序列化器"""

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'gender', 'dob', 'role', 'date_joined', 'last_login'
        )
        read_only_fields = ('id', 'username', 'role',
                            'date_joined', 'last_login')


class ChangePasswordSerializer(serializers.Serializer):
    """修改密碼序列化器"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """驗證密碼"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("新密碼與確認密碼不匹配")
        return attrs

    def validate_old_password(self, value):
        """驗證舊密碼"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("舊密碼錯誤")
        return value
