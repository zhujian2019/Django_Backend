# POST /meiduo_admin/authorizations/
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer

# class AdminAuthView(APIView):
#
#     def post(self, request):
#         '''
#         管理员登录
#         :param request:
#         :return:
#         '''
#         # 1.获取参数并进行校验
#         serializer = AdminAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#
#
#         # 2.创建生成jwt token
#         serializer.save() # 调用序列化器类中的create
#
#         # 3.将用户数据序列化并返回
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# 代码优化
# class AdminAuthView(CreateModelMixin, GenericAPIView):
from users.models import User


class AdminAuthView(CreateAPIView):
    # 指定视图所使用的序列化器类
    serializer_class = AdminAuthSerializer


# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
# class UserInfoView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         '''
#         获取普通用户数据
#         :param request:
#         :return:
#         {
#             "counts": "用户总量",
#             "lists": [
#                 {
#                     "id": "用户id",
#                     "username": "用户名",
#                     "mobile": "手机号",
#                     "email": "邮箱"
#                 },
#                 ...
#             ],
#             "page": "页码",
#             "pages": "总页数",
#             "pagesize": "页容量"
#         }
#         '''
#         # 1.获取keyword关键字
#         keyword = request.query_params.get('keyword')
#
#         # 2.查询普通用户数据
#         if keyword is None or keyword == '':
#             users = User.objects.filter(is_staff=False)
#         else:
#             users = User.objects.filter(is_staff=False, username__contains=keyword)
#
#         # 3.将用户数据序列化返回
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

# 代码优化1
# class UserInfoView(GenericAPIView):
# class UserInfoView(ListAPIView):
#     permission_classes = [IsAdminUser]
#
#     # 指定视图所使用的序列化器类
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         '''返回视图所使用的查询集'''
#         # 1.获取keyword关键字
#         keyword = self.request.query_params.get('keyword')
#
#         # 2.查询普通用户数据
#         if keyword is None or keyword == '':
#             users = User.objects.filter(is_staff=False)
#         else:
#             users = User.objects.filter(is_staff=False, username__contains=keyword)
#
#         return users
#
#     # def get(self, request):
#     #     '''
#     #     获取普通用户数据
#     #     :param request:
#     #     :return:
#     #     '''
#     #     # 查询普通用户数据
#     #     users = self.get_queryset()
#     #
#     #     # 将用户数据序列化并返回
#     #     serializer = self.get_serializer(users, many=True)
#     #     return Response(serializer.data)
#
#
#     # POST /meiduo_admin/users/
#     def post(self, request):
#         '''
#         新增用户数据
#         :param request:
#         :return:
#         '''
#         # 1.获取参数并进行校验
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # 2.创建并保存新用户数据
#         serializer.save()
#
#         # 3.将新用户数据序列化并返回
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# 代码优化2
class UserInfoView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图所使用的查询集
    serializer_class = UserSerializer

    def get_queryset(self):
        '''返回视图所使用的查询集'''
        # 1.获取keyword关键字
        keyword = self.request.query_params.get('keyword')

        # 2.查询普通用户数据
        if keyword is None or keyword == '':
            users = User.objects.filter(is_staff=False)
        else:
            users = User.objects.filter(is_staff=False, username__contains=keyword)

        return users

