import random
from web import models
from django import forms
from utils.encrypt import md5
from django.core.validators import ValidationError, RegexValidator
from utils.send_code import send_msg
from django_redis import get_redis_connection


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(
        label="密码",
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符'
        },
        widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="重置密码", min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': '密码长度不能小于8个字符',
                                           'max_length': '密码长度不能大于64个字符'
                                       }, widget=forms.PasswordInput())
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'code']

    def clean_username(self):
        username_input = self.cleaned_data.get('username')
        exists = models.UserInfo.objects.filter(username=username_input).exists()
        if exists:
            raise ValidationError('用户名已存在！')
        return username_input

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError('密码不一致')
        return confirm_pwd

    def clean_email(self):
        email_input = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email_input).exists()
        if exists:
            raise ValidationError('邮箱已注册！')
        return email_input

    def clean_code(self):
        code_input = self.cleaned_data.get('code')
        email = self.cleaned_data.get('email')
        if not email:
            return code_input
        coon = get_redis_connection('default')
        redis_code = coon.get(email)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code = redis_code.decode('utf-8')
        if code_input.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')
        return code_input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


# class SendCodeForm(forms.Form):
#     type = forms.CharField(label='类型')  # form中把需要校验的字段都建立，但是因为表单里没有type栏，所以type的结果也并到了email里
#     email = forms.EmailField(label='邮箱')
#     # 这里字段的创建顺序也有讲究，type要创建在之前，因为钩子函数只要email的，type创建在前面，执行clean_email的时候，type已经clean过了
#     def clean_email(self):
#         # print(self.cleaned_data)   #  {'type': ['register'], 'email': ['406684614@qq.com'], }
#         email_input = self.cleaned_data.get('email')
#         exists = models.UserInfo.objects.filter(email=email_input).exists()
#         if exists:
#             raise ValidationError("邮箱已注册！")
#         type_input = self.cleaned_data.get('type')
#         if type_input not in ['register', 'login', 'reset']:
#             raise ValidationError('模板格式错误')
#         return email_input

# 还有一种方法，在不创建type字段的前提下，如何在类定义中，调用type字段，重写初始化方法，传入request参数
class SendCodeForm(forms.Form):
    email = forms.EmailField(label='邮箱')

    # 重写init方法，该类没有init方法，会执行父类（forms.form）的init方法，这里加上一个参数request，对应实例form对象可以传进来
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_email(self):
        # 判断邮箱是否已经存在
        email_input = self.cleaned_data.get('email')
        exists = models.UserInfo.objects.filter(email=email_input).exists()
        if exists:
            raise ValidationError("邮箱已注册！")

        # 判断模板是否正确
        type_input = self.request.GET.get('type')
        if type_input not in ['register', 'login', 'reset']:
            raise ValidationError('模板格式错误')

        # 发短信&写入redis, 为了将发短信失败的信息也在钩子里呈现
        code = random.randint(100000, 999999)
        result = send_msg(email_input, code, type_input)
        if not result['status']:
            raise ValidationError(f"验证码发送失败，{result['errmsg']}")
        # 验证码写入redis（django-redis)
        coon = get_redis_connection('default')
        coon.set(email_input, code, ex=60)

        return email_input
