from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.users import GoodsVisitSerializer
from users.models import User


# GET /meiduo_admin/statistical/total_count/
class UserTotalCountView(APIView):
    # 在请求头传参 jwt token 验证用户
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取网站总用户数量
        :param request:
        :return:
        '''
        # 1.统计网站用户的数量
        count = User.objects.count()

        # 2.将用户数量返回
        now_date = timezone.now()

        response_date = {
            'count': count,
            'date': now_date.date()
        }

        return Response(response_date)


# GET /meiduo_admin/statistical/day_increment/
class UserDayCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, reuqest):
        '''
        获取网站日增用户数量
        :param reuqest:
        :return:
        '''
        # 1.统计网站日增用户
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_date).count()

        # 2.返回响应数据
        response_data = {
            'date': now_date.date(),
            'count': count
        }
        return Response(response_data)


# GET /meiduo_admin/statistical/day_active/
class UserActiveAcountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取日活跃用户数量
        :param request:
        :return:
        '''
        # 1. 获取日活用户量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()

        # 2. 返回应答
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/day_orders/
class UserOrderCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取日下单用户数量
        :param request:
        :return:
        '''
        # 1. 获取日下单用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()

        # 2. 返回应答
        response_data = {
            'date': now_date.date(),
            'count': count
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/month_increment/
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取近30天每天新增用户数量
        :param request:
        :return:
        '''
        # 1.统计近30天每天新增用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 统计起始日期
        begin_date = now_date - timezone.timedelta(days=29)

        # 统计数据列表
        count_list = []

        # 0-29
        for i in range(30):
            # 当天日期
            cur_date = begin_date + timezone.timedelta(days=i)
            # 次日日期
            next_date = cur_date + timezone.timedelta(days=1)

            # 统计当天新增用户数量
            count = User.objects.filter(date_joined__gte=cur_date, date_joined__lt=next_date).count()

            count_list.append({
                'date': cur_date.date(),
                'count': count
            })

        # 2.返回
        return Response(count_list)



#  GET /meiduo_admin/statistical/goods_day_views/
class GoodsDayView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        获取当日分类商品访问量
        :param request:
        :return:
        '''
        # 1.查询获取当日分类商品访问量
        # 当前日期
        now_date = timezone.now().date()

        goods_visit = GoodsVisitCount.objects.filter(date=now_date)

        # 2.将查询数据序列化并返回
        serializer = GoodsVisitSerializer(goods_visit, many=True)
        return Response(serializer.data)


