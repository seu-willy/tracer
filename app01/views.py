from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from utils.send_code import send_msg
from app01 import models
from django import forms
from django.views.decorators.csrf import csrf_exempt
from utils.encrypt import md5
from django.core.validators import ValidationError

@csrf_exempt
def send_code(request):
    type = request.GET.get('type')
    to_email = request.POST.get('email')
    code_register = send_msg(to_email, type)
    request.session['code_register'] = code_register
    return JsonResponse({'status':True})


class UserInfo(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label="重置密码", widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='验证码', widget=forms.TextInput)

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'code']

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('密码不一致')
        return confirm_pwd


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
        return render(request, "app01/register.html", {'form':form})
    form2 = UserInfo(data=request.POST)
    if form2.is_valid():
        code_input = form2.cleaned_data.get('code')
        code_row = request.session.get('code_register')
        print(code_input)
        print(code_row)
        if str(code_input) != str(code_row):
            form2.add_error('code', '验证码错误')
            return render(request, "app01/register.html", {'form': form2})
        form2.save()
        return HttpResponse('注册成功')
    return render(request, "app01/register.html", {'form':form2})