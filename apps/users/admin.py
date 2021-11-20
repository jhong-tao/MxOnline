from django.contrib import admin
from django.contrib.auth.admin import UserAdmin     # UserAdmi为Django内部自带的后台用户管理器

from apps.users.models import UserProfile


# admin.py是用来注册app的model的，也就是用来注册数据库中的表，方便后台管理系统来管理


class UserProfileAdmin(admin.ModelAdmin):
    """
    用户表管理器
    """
    pass


# 通过admin.site.register方法将用户表UserProfile用户表注册到后台管理系统中去，UserAdmin用户后台管理器
admin.site.register(UserProfile, UserAdmin)
