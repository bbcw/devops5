from django import forms
from django.contrib.auth.models import ContentType

class CreatePermissionForms(forms.Form):
    content_type= forms.IntegerField(required=True)
    codename    = forms.CharField(required=True)
    name        = forms.CharField(required=True)

    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        if codename.find(" ") >= 0:
            raise forms.ValidationError("codename 不能有空格")
        return codename

    def clean_content_type(self):
        content_type = self.cleaned_data.get("content_type")
        try:
            ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("模型不存在")
        return content_type

