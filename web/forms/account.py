
from web import models
from django import forms
from utils.encrypt import md5
from django.core.validators import ValidationError

class RegisterModelForm(forms.ModelForm):
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