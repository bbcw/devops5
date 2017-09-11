from django.db import models
from django.contrib.auth.models import User
# Create your models here.

"""用户model的扩展 是auth_user的外链"""
class Profile(models.Model):
    user    = models.OneToOneField(User, verbose_name="与User模型是一对一关系")
    name    = models.CharField("中文名",max_length=32)
    phone   = models.CharField("电话号码", max_length=20)
    weixin  = models.CharField("weixin id", max_length=50)
