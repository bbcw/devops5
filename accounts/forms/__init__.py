#!/usr/bin/python
# coding=utf8
from django import forms
from resources.idc import Idc
from django.contrib.auth.models import ContentType


class CreatePermissionForm(forms.Form):
    """验证新增权限的表单"""
    content_type = forms.IntegerField(required=True)
    codename = forms.CharField(required=True)
    name = forms.CharField(required=True)


    # 自定义字段级别验证方式
    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        if codename.find(" ") >= 0:
            raise forms.ValidationError("codename 不能有空格")
        return codename

    def clean_content_type(self):
        content_type_id = self.cleaned_data.get("content_type")

        try:
            return ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("模型不存在")


class CreateGroupForm(forms.Form):
    """创建用户组表单"""
    name = forms.CharField(required=True)

    # 自定义 name 字段验证，不能有空格
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name.find(" ") >= 0:
            raise forms.ValidationError("name 字段不能有空格")
        return name