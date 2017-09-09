from django.db import models

# Create your models here.

class Idc(models.Model):
    """
    IDC数据表字段
    """
    name = models.CharField("idc 字母简称", max_length=10, default="", unique=True)
    idc_name = models.CharField("idc 中文名字",max_length=100, default="")
    address = models.CharField("具体的地址，阿里云", max_length=255, default="")
    phone = models.CharField("机房负责人联系电话", max_length=20, null=True)
    email = models.EmailField("机房联系email", null=True)
    username = models.CharField("机房联系人", max_length=32, null=True)

    ##定义此模块使用的数据表名称
    class Meta:
        db_table = "resources_idc"