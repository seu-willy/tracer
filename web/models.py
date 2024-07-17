from django.db import models

class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)  # db_index=True可以创建索引，查询速度快
    password = models.CharField(verbose_name="密码", max_length=32)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
