'''
用户相关的功能：注册、登录、注销
'''
import datetime
import uuid
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendCodeForm, LoginCodeForm, LoginForm
from web import models
from utils.code import check_code
from django_redis import get_redis_connection
from io import BytesIO
from django.db.models import Q


def register(request):
    '''用户注册'''
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库
        # instance = form.save()  save会把数据库没有的字段剔除
        # instance = models.UserInfo.objects.create(**form.cleaned_data)
        instance = form.save()

        # 创建交易记录
        price_object = models.PriceStrategy.objects.filter(category=1, title='个人免费版').first()
        models.TradeInfo.objects.create(
            oid=uuid.uuid4(),
            status=2,
            user=instance,
            price_strategy=price_object,
            count=0,
            pay=0,
            start_time=datetime.datetime.now(),
        )

        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login_code(request):
    '''邮箱登录'''
    if request.method == 'GET':
        form = LoginCodeForm()
        return render(request, 'login_code.html', {'form': form})
    form = LoginCodeForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user_object = models.UserInfo.objects.filter(email=email).first()
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)

        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    '''用户名密码登录'''
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        # 基于Q完成的复杂的选择条件，邮箱和用户名都可以登录
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(
            password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('/index/')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def logout(request):
    '''退出登录'''
    request.session.clear()
    return redirect('index')


def send_code(request):
    '''发送邮箱验证码'''
    form = SendCodeForm(request, request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def image_code(request):
    '''生成图片验证码'''
    img, code_string = check_code()  # 调用函数生成验证码和图片
    request.session['image_code'] = code_string  # 将验证码写入session，方便在登录的地方验证，有点像实例属性，大家都能用
    request.session.set_expiry(60)  # 给session设置时长，这里是为了避免验证图片一直有效
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
