'''
用户相关的功能：注册、登录、注销
'''
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from web.forms.account import RegisterModelForm, SendCodeForm
from web import models


def register(request):
    title = '注册'
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form, 'title':title})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库
        # instance = form.save()  save会把数据库没有的字段剔除
        # instance = models.UserInfo.objects.create(**form.cleaned_data)
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def send_code(request):
    print(request.GET)
    form = SendCodeForm(request, request.GET)
    print(form)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
