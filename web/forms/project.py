from django import forms
from web.forms.BootstrapForm import BootstrapForm
from web import models
from django.core.validators import ValidationError


class ProjectModelForm(BootstrapForm, forms.ModelForm):
    # bootstrap_exclude_fields = ['color']
    # detail = forms.CharField(label='项目描述', max_length=255, widget=forms.Textarea(attrs={'xx':123})) 方式一重写属性
    class Meta:
        model = models.ProjectInfo
        fields = ['name', 'color', 'detail']
        widgets = {
            'detail': forms.Textarea,
            # 'color':forms.CheckboxInput
        }  # 方式二 重写属性

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        '''项目校验'''
        name_input = self.cleaned_data.get('name')
        # 1、项目是否创建过,要加creator判定，不然所有人都不能项目同名
        exists = models.ProjectInfo.objects.filter(name=name_input, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目已存在，请勿重复创建！')
        # 2、用户是否有额度
        count_max = self.request.tracer.price_strategy.project_num
        num = models.ProjectInfo.objects.filter(creator=self.request.tracer.user).count()
        print(count_max, num)
        if num >= count_max:  # 这里有等号
            raise ValidationError('已超过最大创建项目数，请购买套餐')

        return name_input
