'''
用户相关的功能：注册、登录、注销
'''
from django.shortcuts import render
from web.forms.account import RegisterModelForm
def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form':form})