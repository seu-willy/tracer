from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from utils.send_code import send_msg
from app01 import models
from django import forms
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_code(request):
    type = request.GET.get('type')
    to_email = request.POST.get('email')
    send_msg(to_email, type)
    return JsonResponse({'status':True})


class UserInfo(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label="重置密码", widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='验证码', widget=forms.TextInput)

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'code']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
def register(request):
    if request.method == "GET":
        form = UserInfo()
        return render(request, "register.html", {'form':form})
    form2 = UserInfo(data=request.POST)
