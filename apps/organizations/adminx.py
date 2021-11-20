#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> adminx.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：adminx.py文件的名称是固定的，用来把app中的相关的表注册到xadmin后台管理系统中
==================================================
"""
import xadmin
from apps.organizations.models import Teacher, CourseOrg, City


class TeacherAdmin(object):
    """
    TeacherAdmin：教师后台管理器
    """
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    """
    CourseOrgAdmin:课程机构后台管理器
    """
    list_display = ['name', 'desc', 'click_nums']
    search_fields = ['name', 'desc', 'click_nums']
    list_filter = ['name', 'desc', 'click_nums']
    style_fields = {
        "desc": "ueditor"
    }


class CityAdmin(object):
    """
    CityAdmin:城市后台管理器
    """
    list_display = ['id', 'name', 'desc']  # list_display用来定义在xadmin后台管理系统的列表中显示的字段名称，这些字段必须是表里有的
    search_fields = ['name', 'desc']  # search_fields用来定义在xadmin后台管理系统的列表中可以搜索的字段名称
    list_filter = ['name', 'desc', 'add_time']  # list_filter来定义在xadmin后台管理系统的列表中可以过滤的字段名称
    list_editable = ['name', 'desc']  # list_editable用来定义在xadmin后台列表中能直接修改的字段


xadmin.site.register(Teacher, TeacherAdmin)  # 将 Teacher表注册到xadmin后台管理系统中
xadmin.site.register(CourseOrg, CourseOrgAdmin)  # 注册CourseOrg到xadmin后台管理系统
xadmin.site.register(City, CityAdmin)  # 注册CourseOrg到xadmin后台管理系统
