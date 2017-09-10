from django import forms
from resources.models import Idc

class CreateIdcForm(forms.Form):
    name = forms.CharField(required=True) 
    idc_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, error_messages={"invalid":"format is error"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            Idc.objects.get(name__exact=name)
            raise forms.ValidationError("idc really exist!!!")
        except Idc.DoesNotExist:
            return name

    def clean(self):
        data = self.cleaned_data
        # data["other"] = "xxxxxxxx"
        return data
        
