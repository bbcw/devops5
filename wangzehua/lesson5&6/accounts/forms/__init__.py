from django import forms
from django.contrib.auth.models import ContentType

class CreatePermissionForm(forms.Form):
    #字段级别验证
    content_type        = forms.IntegerField(required=True)
    codename            = forms.CharField(required=True)
    name                = forms.CharField(required=True)

    #自定义字段验证,所有数据在cleaned_data里
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

    #针对所有数据进行验证
    def clean(self):
        pass


