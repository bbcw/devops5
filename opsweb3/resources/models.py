from django.db import models


class Idc(models.Model):
    name = models.CharField("字母简称", max_length=10, default="", unique=True)
    idc_name = models.CharField("中文名", max_length=128, default="")
    address = models.CharField("具体地址, 云厂商可以为空", max_length=128, null=True)
    username = models.CharField("联系人", max_length=10, null=True)
    user_phone = models.CharField("联系人电话", max_length=20, null=True)
    email = models.EmailField("联系人Email", null=True)

    class Meta:
        db_table = "resources_idc"
        permissions = (
            ("view_idc", "查看idc"),
        )


# class UserInfo(models.Model):
#     name = models.CharField("用户名", max_length=32, unique=True)
#     address = models.CharField("地址", max_length=64, null=True)
#     phone = models.CharField("联系方式", max_length=20, null=True)