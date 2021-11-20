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
from apps.courses.models import Course, Lesson, Video, CourseResource


# 配置xadmin的全局信息，在任意一个app的adminx文件中配置都可以
class XAdminGlobalSettings(object):
    """
    XAdminGlobalSetting:xadmin后台全局配置
    """
    site_title = '慕学后台管理系统'  # site_title：设置xadmin后台管理系统标题, 变量名是固定的不能随便命名
    site_footer = '慕学在线网'  # sete_title：设置xadmin后台管理系统页面底部，变量名是固定的不能随便命名
    # menu_style = 'accordion'  # 侧边栏菜单折叠功能


class XAdminBaseSettings(object):
    """
    配饰xadmin主题，变量名都是固定的
    """
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    """
    CourseAdmin:课程后台管理器
    """
    # list_display用来定义在xadmin后台管理系统的列表中显示的字段名称，这些字段必须是表里有的
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']  # search_fields用来定义在xadmin后台管理系统的列表中可以搜索的字段名称
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times',
                   'students']  # list_filter来定义在xadmin后台管理系统的列表中可以过滤的字段名称
    list_editable = ['name', 'desc', 'degree']  # list_editable用来定义在xadmin后台列表中能直接修改的字段


class LessonAdmin(object):
    """
    LessonAdmin:后台章节管理器
    """
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    """
    VideoAdmin：后台视频管理器
    """
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    """
    CourseResourceAdmin:后台课程资源管理器
    """
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']


xadmin.site.register(Course, CourseAdmin)  # 将 Course相关的表注册到xadmin后台管理系统中
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, XAdminGlobalSettings)   # 将xadmin后台管理系统的全局配置注册到后台
xadmin.site.register(xadmin.views.BaseAdminView, XAdminBaseSettings)   # 将xadmin后台管理系统的主题配置注册到后台
