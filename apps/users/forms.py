#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> forms.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：前端form表单验证
==================================================
"""
from django import forms        # forms.Form类，是django提供来专门用来做表单验证的类
from captcha.fields import CaptchaField  # CaptchaField,为captcha自定义的一种数据类型

from apps.utils.db_utils import redis_get
from apps.users.models import UserProfile


class RegisterPostForm(forms.Form):
    """
    RegisterPostForm 用来完成用户注册时图片验证码验证，用户名（手机号码），密码的验证
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)  # 验证手机号码
    code = forms.CharField(required=True, min_length=4, max_length=4)  # 验证图片验证码
    password = forms.CharField(required=True)  # 验证密码

    def clean_mobile(self):
        """
        clean_mobile 验证手机号码是否存在，存在则不能注册
        :return:
        """
        mobile = self.data.get('mobile')
        # 如果短信验证码与redis中一致，则验证用户是否存在
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError('手机号码已注册')  # 如果手机号码存在则不能注册
        return mobile

    def clean_code(self):
        """
        验证短信验证码和redis中是否一致
        redis_get提供的clean_字段名称，可以实现对特定的每个字段进行单独验证，返回单独的字段异常信息
        clean_code会比clean先执行，所以在clean_code这个函数里不能通过cleaned_data来获取某个字段的值，只能到data变量中去取值最初的值
        :return:
        """
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        # 验证前端form传递过来的短信验证码与服务器的redis中存放的验证码是否一致
        if code != redis_get(mobile):
            raise forms.ValidationError('验证码不正确')  # 验证码不一样，抛出异常
        return code  # 验证码一样 返回form表单数据



class RegisterGetForm(forms.Form):
    """
    注册的时候用来生成图片验证码
    """
    captcha = CaptchaField()  # 生成前端js中ajax请求的图片验证码


class LoginForm(forms.Form):
    """
    用户登录表单验证:
    这里定义的成员变量username，password必须要与前端登录页面中form表单中的定义的输入框的name属性值一致
    """
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    """
    图片动态验证码登录，表单验证
    """
    captcha = CaptchaField()  # 生成前端js中ajax请求的图片验证码
    mobile = forms.CharField(required=True, min_length=11, max_length=11)  # 校验js中ajax提交的手机号码


class DynamicLoginPostForm(forms.Form):
    """
    短信验证码，表单验证
    """
    # 直接写的成员变量，是用来验证前端form提交过来的数据是否存在和合法
    mobile = forms.CharField(required=True, min_length=11, max_length=11)  # 手机号码表单验证
    code = forms.CharField(required=True, min_length=4, max_length=4)  # 图片验证码

    # 重写forms.Form的clean方法，用来完成自定义的前端提交的表单数据的验证
    def clean(self):
        """
        redis_get提供的clean 方法是在对前面的字段进行验证后，在进行总的验证，不能返回具体哪一个字段的错误信息
        :return:
        """
        # cleaned_data中包含了所有的前端form表单提交过来的每一个字段的信息，cleaned_data中的值是调用过clean进行数据验证后生成的
        mobile = self.cleaned_data['code']
        code = self.cleaned_data['code']
        # 验证前端form传递过来的短信验证码与服务器的redis中存放的验证码是否一致
        if code != redis_get(mobile):
            raise forms.ValidationError('验证码不正确')  # 验证码不一样，抛出异常
        return self.cleaned_data  # 验证码一样 返回form表单数据

    def clean_code(self):
        """
        redis_get提供的clean_字段名称，可以实现对特定的每个字段进行单独验证，返回单独的字段异常信息
        clean_code会比clean先执行，所以在clean_code这个函数里不能通过cleaned_data来获取某个字段的值，只能到data变量中去取值最初的值
        :return:
        """
        mobile = self.data.get('mobile')
        code = self.data.get('code')
        # 验证前端form传递过来的短信验证码与服务器的redis中存放的验证码是否一致
        if code != redis_get(mobile):
            raise forms.ValidationError('验证码不正确')  # 验证码不一样，抛出异常
        return self.cleaned_data  # 验证码一样 返回form表单数据