import datetime

from web import models
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings

class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_strategy = None

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        '''如果用户已登录，在request中赋值'''
        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 对白名单的url，可以直接访问
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        # 不在白名单中的需要判断是否登录
        # 如果没有登录回到登录页面
        if not request.tracer.user:
            return redirect('login')

        # 登录后在request中附加项目额度
        # 方式一:对应要在用户注册时生成一条免费额度的支付记录
        # 获取登录对象的交易订单对象最后一个
        trade_object = models.TradeInfo.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否已过期
        current_time = datetime.datetime.now()
        if trade_object.end_time and trade_object.end_time < current_time:
            trade_object = models.TradeInfo.objects.filter(user=user_object, status=2, price_strategy__category=1).first()

        request.tracer.price_strategy = trade_object.price_strategy # price_strategy是个foreign对象，获取到对应表的一行对象
        # # 方式二
        # # 获取登录对象的交易订单对象最后一个
        # trade_object = models.TradeInfo.objects.filter(user=user_object, status=2).order_by('-id').first()
        # if not trade_object:  # 因为方式二不需要在注册生成免费额度订单，所以如果用户没有付费，则不存在
        #     request.price_strategy = models.PriceStrategy.objects.filter(category=1, title='个人免费版').first()
        # else:  # 付费了，要判断是否过期
        #     # 判断是否已过期
        #     current_time = datetime.datetime.now()
        #     if trade_object.end_time and trade_object.end_time < current_time:
        #         request.price_strategy = models.PriceStrategy.objects.filter(category=1, title='个人免费版').first()
        #     else:
        #         request.price_strategy = trade_object.price_strategy