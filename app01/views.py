from django.shortcuts import render, HttpResponse
from utils.send_code import send_msg
from app01 import models

def send_code(request):
    to_email = '406684614@qq.com'
    type = 'register'
    send_msg(to_email, type)
    return HttpResponse("发送成功")

class UserInfo(models):
    class Meta:
        model = models.UserInfo
        fields = ""

def register(request):

    return render(request, "register.html")
