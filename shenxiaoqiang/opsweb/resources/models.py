# coding:utf8
from django.db import models

# Create your models here.

class Idc(models.Model):
    name = models.CharField("idc 简称", max_length=10, default="", db_index=True, unique=True)
    idc_name = models.CharField("idc 名字", max_length=50, default="")
    address = models.CharField("address", max_length=255, null=True)
    phone = models.CharField("idc phone", max_length=20, null=True)
    email = models.EmailField("idc email", null=True)
    username = models.CharField("idc 联系人",max_length=32, null=True)
    remark = models.CharField("remark", max_length=100, default="")

    class Meta:
        db_table = "resources_idc"
        permissions = (
            ("view_idc", "can show idc list"),
        )

class Serstatus(models.Model):
    name = models.CharField("服务器状态",max_length=20, default="")

class Server(models.Model):
    ser_status      = models.ForeignKey(Serstatus,related_name="Serstatus", null=True)
    supplier        = models.IntegerField(null=True)
    manufacturers   = models.CharField(max_length=50, null=True)
    manufacture_date= models.DateField(null=True)
    server_type     = models.CharField(max_length=50, null=True)
    sn              = models.CharField(max_length=60, db_index=True, null=True)
    idc             = models.ForeignKey(Idc, null=True)
    os              = models.CharField(max_length=50, null=True)
    hostname        = models.CharField(max_length=50, db_index=True, null=True)
    inner_ip        = models.CharField(max_length=32, null=True, unique=True)
    mac_address     = models.CharField(max_length=50, null=True)
    ip_info         = models.CharField(max_length=255, null=True)
    server_cpu      = models.CharField(max_length=250, null=True)
    server_disk     = models.CharField(max_length=100, null=True)
    server_mem      = models.CharField(max_length=100, null=True)
    status          = models.CharField(max_length=100,db_index=True, null=True)
    remark          = models.TextField(null=True)
    service_id      = models.IntegerField(db_index=True, null=True)
    server_purpose  = models.IntegerField(db_index=True, null=True)
    check_update_time = models.DateTimeField(auto_now=True, null=True)
    vm_status       = models.IntegerField(db_index=True, null=True)
    uuid            = models.CharField(max_length=100, db_index=True,null=True)


    def __str__(self):
        return "{} [{}]".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = 'resources_server'
        ordering = ['id']

class Product(models.Model):
    service_name = models.CharField("业务线", max_length=32)
    module_letter = models.CharField("业务线简称", max_length=30, db_index=True)
    op_interface = models.CharField("OPS", max_length=150)
    dev_interface = models.CharField("业务对接人", max_length=150)
    pid = models.IntegerField("上级业务ID", db_index=True)

    def __str__(self):
        return self.service_name

