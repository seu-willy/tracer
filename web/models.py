from django.db import models

class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)  # db_index=True可以创建索引，查询速度快
    password = models.CharField(verbose_name="密码", max_length=32)
    email = models.EmailField(verbose_name="邮箱", max_length=32)

class PriceStrategy(models.Model):
    '''价格策略表'''
    category_choice = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他')
    )
    category = models.SmallIntegerField(verbose_name='收费类型',default=1, choices=category_choice)
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')
    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class TradeInfo(models.Model):
    '''用户订单表'''
    oid = models.CharField(verbose_name='交易订单', max_length=128, unique=True)
    status_choice = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='支付状态', choices=status_choice)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    price_strategy = models.ForeignKey(verbose_name='价格策略', to='PriceStrategy')
    count = models.SmallIntegerField(verbose_name='数量', help_text='0表示无期限')
    pay = models.IntegerField(verbose_name='实际支付价格')
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class ProjectInfo(models.Model):
    '''项目表'''
    name = models.CharField(verbose_name='项目名称', max_length=32)
    color_choice = (
        (1, '#56b8eb'),
        (2, '#f28033'),
        (3, '#ebc656'),
        (4, '#a2d148'),
        (5, '#20BFA4'),
        (6, '#7461c2'),
        (7, '#20bfa3')
    )
    color = models.SmallIntegerField(verbose_name='项目颜色', choices=color_choice, default=1)
    detail = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='项目已使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)
    join_count = models.IntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建人', to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class ProjectTeamInfo(models.Model):
    '''项目成员表'''
    user = models.ForeignKey(verbose_name='参与成员', to='UserInfo')
    project = models.ForeignKey(verbose_name='项目', to='ProjectInfo')
    star = models.BooleanField(verbose_name='星标', default=False)
    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)