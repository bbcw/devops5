from django import forms
from django.contrib.auth.models import ContentType, Permission, Group

class CreateGroupForm(forms.Form):
    name = forms.CharField(required=True)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            Group.objects.get(name__exact=name)
            raise forms.ValidationError("用户组已经存在")
        except Group.DoesNotExist:
            pass
        return name

class CreatePermissionForm(forms.Form):
    content_type = forms.IntegerField(required=True)
    codename     = forms.CharField(required=True)
    name         = forms.CharField(required=True)

    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        if codename.find(" ") >=0 :
            raise forms.ValidationError("codename 不能有空格")
        try:
            Permission.objects.get(codename__exact=codename)
            raise forms.ValidationError("codename 已经存在")
        except Permission.DoesNotExist:
            pass
        return codename

    def clean_content_type(self):
        content_type_id = self.cleaned_data.get("content_type")
        try:
            return ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("模型不存在")