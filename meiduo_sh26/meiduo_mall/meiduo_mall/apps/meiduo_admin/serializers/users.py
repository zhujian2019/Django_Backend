import re

from django.utils import timezone
from rest_framework import serializers

from goods.models import GoodsVisitCount
from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    '''Admin序列化器类'''
    token = serializers.CharField(label='JWT token', read_only=True)
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def validate(self, attrs):
        # 用户名和密码是否正确
        username = attrs['username']
        password = attrs['password']

        try:
            # is_staff=True说明是管理员
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 用户存在，检验密码
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # 获取user
        user = validated_data['user']

        # 更新最新登录时间
        user.last_login = timezone.now()
        user.save()

        # 生成创建jwt token
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 给user对象增加属性token，保存登录用户身份信息
        user.token = token

        return user


class GoodsVisitSerializer(serializers.ModelSerializer):
    '''分类商品浏览序列化器类'''
    # 关联对象嵌套序列化：将关联对象序列化为关联对象模型类__str__方法
    category = serializers.StringRelatedField(label='分类')

    class Meta:
        model = GoodsVisitCount
        fields = ('category', 'count')


class UserSerializer(serializers.ModelSerializer):
    '''用户序列化器类'''

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为5',
                    'max_length': '用户名最大长度为20'
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为8',
                    'max_length': '密码最大长度为20'
                }
            }
        }

    def validated_mobile(self, value):
        '''手机号格式，手机号是否注册'''
        # 手机格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        # 手机号是否注册
        res = User.objects.filter(mobile=value).count()

        if res > 0:
            raise serializers.ValidationError('手机号已注册')

        return value

    def create(self, validated_data):
        '''创建并保存新用户数据'''
        user = User.objects.create_user(**validated_data)
        return user
