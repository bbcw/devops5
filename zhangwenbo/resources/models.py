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
    # class Meta:
    #     db_table = "resources_idc"
class Statuses(models.Model):
    status_mark = models.CharField("状态标签", max_length=255)


class Server(models.Model):
    supplier        = models.IntegerField(null=True)
    manufacturers   = models.CharField(max_length=50, null=True)
    manufacture_date= models.DateField(null=True)
    server_type     = models.CharField(max_length=100, null=True)
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
    statuses        = models.ForeignKey(Statuses, max_length=100,db_index=True, null=True)
    remark          = models.TextField(null=True)
    service_id      = models.IntegerField(db_index=True, null=True)
    server_purpose  = models.IntegerField(db_index=True, null=True)
    check_update_time = models.DateTimeField(auto_now=True, null=True)
    vm_status       = models.IntegerField(db_index=True, null=True)
    uuid            = models.CharField(max_length=100, db_index=True,null=True)


    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'resources_server'
        ordering = ['id']



class Product(models.Model):
    service_name    = models.CharField("业务线的名字", max_length=32)
    module_letter   = models.CharField("业务线字母简称", max_length=10, db_index=True)
    op_interface    = models.CharField("运维对接人", max_length=150)
    dev_interface   = models.CharField("业务对接人", max_length=150)
    pid             = models.IntegerField("上级业务线id", db_index=True)

    def __str__(self):
        return self.service_name