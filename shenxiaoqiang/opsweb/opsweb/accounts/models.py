from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="与User表一对一关系")
    cname = models.CharField("中文名", max_length=32)
    phone = models.CharField("电话", max_length=20)
    weixin = models.CharField("weixin", max_length=50)

#    class Meta:
#        db_table = "profile"
