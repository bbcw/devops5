# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="与User模型是一对一关系")
    name = models.CharField("中文名", max_length=32)
    phone = models.CharField("电话号码", max_length=20)
    wechat = models.CharField("微信号", max_length=50)

    class Meta:
        db_table = "user_profile"
