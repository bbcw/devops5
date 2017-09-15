from django import forms
from django.contrib.auth.models import Group

class CreateGroupForm(forms.Form):
    #字段级别验证
    name        = forms.CharField(required=True)

    #自定义字段验证,所有数据在cleaned_data里
    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            Group.objects.get(name__exact=name)
            raise forms.ValidationError("Group 名称已存在")
        except Group.DoesNotExist:
            return name