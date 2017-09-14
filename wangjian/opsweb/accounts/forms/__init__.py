from django import forms
from django.contrib.auth.models import ContentType,Group

class CreatePermissionForm(forms.Form):
    content_type    = forms.IntegerField(required=True)
    codename        = forms.CharField(required=True)
    name            = forms.CharField(required=True)

    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        if codename.find(" ") >=0 :
            raise forms.ValidationError("codename 不能有空格 ")
        return codename

    def clean_content_type(self):
        content_type_id = self.cleaned_data.get("content_type")
        try:
            return ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("模型不存在")

class CreateGroupForm(forms.Form):
    name            = forms.CharField(required=True)

    # def clean_group_name(self):
    #     group_name = self.cleaned_data.get("name")
        # if group_name == Group.objects.get(name=group_name):
        #     raise forms.ValidationError("用户组已存在")
        # return group_name
    def clean_group_name(self):
        name = self.cleaned_data.get("name")
        if name == Group.objects.get(name=name):
            raise forms.ValidationError("用户组已存在")
        return name