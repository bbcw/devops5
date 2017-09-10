from django import forms
from django.contrib.auth.models import Group, ContentType

class CreateGroupForm(forms.Form):
    name = forms.CharField(required=True)

    def clean_name(self):
        group_name = self.cleaned_data.get("name")
        try:
            Group.objects.get(name__exact=group_name)
            raise forms.ValidationError("groupname really exist!!!")
        except Group.DoesNotExist:
            return group_name


class CreatePermissionForm(forms.Form):
    content_type = forms.IntegerField(required=True)
    codename = forms.CharField(required=True)
    name = forms.CharField(required=True)


    def clean_codename(self):
        codename = self.cleaned_data.get("codename")

        if codename.find(" ") >=0:
            raise forms.ValidationError("codename format error")
        return codename

    def clean_content_type(self):
        content_type_id = self.cleaned_data.get("content_type")

        try:
            return ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError("model is not exist")
