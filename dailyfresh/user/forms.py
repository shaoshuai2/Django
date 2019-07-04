import re

from django import forms
from django.core.exceptions import ValidationError

from user.models import User


class UserForm(forms.Form):
    user_name = forms.CharField(min_length=6,error_messages={
        'required':'必须输入用户名',
        'min_length':'用户名不能少于6位'
    })
    pwd = forms.CharField(min_length=3,error_messages={
        'required':'必须输入密码',
        'min_length':'密码长度不能小于3位'
    })
    cpwd = forms.CharField(min_length=3,error_messages={
        'required':'必须输入密码',
        'min_length':'密码长度不能小于3位'
    })
    email = forms.CharField(max_length=12,error_messages={
        'max_length':'邮箱错误'
    })

    def clean_user_name(self):
        res = User.objects.filter(username=self.cleaned_data.get('user_name')).exists()
        if res:
            raise ValidationError("用户名重名")
        return self.cleaned_data.get('user_name')
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if re.match(r'\d+$',pwd):
            raise ValidationError("密码不能是纯数字")
        return pwd
    def clean_email(self):
        res = User.objects.filter(email=self.cleaned_data.get('email')).exists()
        if res:
            raise ValidationError("邮箱已被占用")
        else:
            email = self.cleaned_data.get("email")
            res1 = re.match(r'\.com$', email)
            if res1:
                raise ValidationError("邮箱格式错误")
            return email
    def clean(self):
        pwd1 = self.cleaned_data.get('pwd')
        pwd2 = self.cleaned_data.get('cpwd')
        if pwd2 != pwd1:
            raise ValidationError({'cpwd':"两次密码不一致"})
        return self.cleaned_data
