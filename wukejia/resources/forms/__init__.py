from  django import  forms

class CreateIdcForm(forms.Form):
    name =  forms.CharField(required=True,)
    idc_name =  forms.CharField(required=True,)
    address = forms.CharField(required=True,)
    phone = forms.CharField(required=True,)
    username = forms.CharField(required=True,)
    email = forms.EmailField(required=True,)
