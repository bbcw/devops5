from django import forms 


class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={"required":"请输入账号"})
    password = forms.CharField(required=True,error_messages={"required":"请输入密码"})

    


    
