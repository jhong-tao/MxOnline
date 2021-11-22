#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> forms.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：用来做课程机构列表页面的用户咨询表单验证
==================================================
"""
import re

from django import forms

from apps.operations.models import UserAsk


class AddAskForm2(forms.Form):
    """
    一般的表单验证方面，继承Form
    """
    name = forms.CharField(required=True, min_length=2, max_length=20)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=2, max_length=20)


class AddAskForm(forms.ModelForm):
    """
    通过继承ModelForm来实现表单的验证，跟model中的字段保持一致，快速实现对表单数据的验证
    """
    # 自定义验证字段
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    # 对手机号码进行特别的自定义验证
    def clean_mobile(self):
        """
        验证手机号码是否合法
        ^1(3[0-9]|5[0-3,5-9]|7[1-3,5-8]|8[0-9])\d{8}$
        解释：
        ^:代表起始，即手机号码只能以1为开头
        3[0-9]：代表手机号码第二位可以是3，第三位可以是0-9中任意一个数字
        5[0-3,5-9]：代表手机号码第二位也可以是5，第三位是0-3和5-9中的任意一个数字
        在这里，以3开头的，以5开头的，以及以8开头的三种情况，我们用“|”来将他们隔开
        \d：匹配一个数字字符，等价于 [0-9]
        $:终止符，代表不可以再有第12位了
        :return:
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = '^1(3[0-9]|5[0-3,5-9]|7[1-3,5-8]|8[0-9])\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            # 手机号码验证通过，返回合法的手机号码
            return mobile
        else:
            # 手机号码不合法，抛出异常
            raise forms.ValidationError('手机号码不合法', code='mobile_invalid')

    class Meta:
        """
        通过model的数据要求验证
        """
        model = UserAsk  # 在Meta中通过model属性配置form表单要验证的数据是哪个model的
        fields = ['name', 'mobile', 'course_name']  # fields指明UserAsk中的那些字段需要被验证
