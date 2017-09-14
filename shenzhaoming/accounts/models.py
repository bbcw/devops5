from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Person(models.Model):
    #username varchar(32) notnull, null存数据库范畴，blank是数据验证范畴，表单验证
    #unique 唯一
    #
    username = models.CharField(max_length=16, null=False)
    #默认情况下Django会自动添加如下字段
    #id = models.AutoField(primary_key=True)

    #排序
    class Meta:
        #排序列 +正序， -倒序， ?随机排序
        ordering = ["username"]
        #该模型所用的数据表的名称，强烈推荐使用小写
        db_table = "person"

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name='与User模型一对一对应')
    name = models.CharField('中文名称', max_length=32)
    phone = models.CharField('电话号码', max_length=20)