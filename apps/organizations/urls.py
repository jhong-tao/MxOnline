#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> urls.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：配置app的url
==================================================
"""
from django.conf.urls import url
from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView

urlpatterns = [
    # 因为在总urls中添加了org的命名空间，所以在使用name的时候前面要加上org
    # 现在对OrgView.as_view()的访问路径变为了http://127.0.0.1:8000/org/list/
    url(r"^list/$", OrgView.as_view(), name="list"),  # 访问课程机构列表的url
    url(r"^add_ask/$", AddAskView.as_view(), name="add_ask"),  # 课程机构中 咨询的url
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),  # 课程机构的详情页，通过分组的形式(?P<org_id>\d+)传递字典类型参数
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name='teacher'),  # 配置讲师列表页url
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name='course'),  # 配置机构课程列表url
]
