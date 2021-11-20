#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> adminx.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：
==================================================
"""
import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    """
    UserAskAdmin：用户询问后台管理器
    """
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserMessageAdmin(object):
    """
    UserMessageAdmin：用户消息后台管理器
    """
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class CourseCommentsAdmin(object):
    """
    CourseCommentsAdmin:用户评论后台管理器
    """
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavoriteAdmin(object):
    """
    UserFavoriteAdmin:用户收藏后台管理器
    """
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


# 注册模块到后台管理系统
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)