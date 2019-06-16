from django.conf.urls import url

from meiduo_admin.views import statistical
from meiduo_admin.views import users

urlpatterns = [
    url(r'^authorizations/$', users.AdminAuthView.as_view()),
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveAcountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),
    # 用户管理
    url(r'^users/$', users.UserInfoView.as_view()),

]