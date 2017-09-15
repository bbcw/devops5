
from django import forms
from resources.models import Idc

class CreateIdcForm(forms.Form):
    #字段级别验证
    name        = forms.CharField(required=True)
    idc_name    = forms.CharField(required=True)
    address     = forms.CharField(required=True)
    phone       = forms.CharField(required=True)
    email       = forms.EmailField(required=False)
    username    = forms.CharField(required=True)

    #自定义字段验证,所有数据在cleaned_data里
    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            Idc.objects.get(name__exact=name)
            raise forms.ValidationError("idc 简称已存在")
        except Idc.DoesNotExist:
            return name

    #自定义表单验证
    def clean(self):
        data = self.cleaned_data
        #data['other'] = "sdklf"
        return data