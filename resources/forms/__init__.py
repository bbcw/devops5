# coding=utf-8
from django import forms
from resources.idc import Idc
from django.contrib.auth.models import ContentType


class CreateIdcForm(forms.Form):
    """验证 idc 输入的表单"""
    name = forms.CharField(required=True, max_length=10)
    idc_name = forms.CharField(required=True, max_length=32)
    address = forms.CharField(required=True, max_length=255)
    phone = forms.CharField(required=True, max_length=20)
    email = forms.CharField(required=True, max_length=50, error_messages={"invalid": "email 格式不对"})
    username = forms.CharField(required=True, max_length=32)


    # 自定义字段级别验证方法，方法名为【clean_<字段名>】
    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Idc.objects.get(name__exact=name)
            raise forms.ValidationError("idc 简称已存在")
        except Idc.DoesNotExist:
            return name

    def clean(self):
        data = self.cleaned_data
        return data
