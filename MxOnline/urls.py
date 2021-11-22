"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include   # url路由方式支持正则表达式
from django.views.generic import TemplateView  # TemplateView 方法用来渲染一个静态的HTML页面
from django.views.decorators.csrf import csrf_exempt  # csrf_exempt方法用来去除url访问时的csrf_token的验证
from django.views.static import serve  # serve静态文件处理的方法


import xadmin

from apps.users.views import LoginView, RegisterView, LogoutView, SendSmsView, DynamicLoginView
from apps.organizations.views import OrgView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),  # 配置captcha图像验证码工具，所有以captcha开头的url都定向到captcha.urls文件中
    path('xadmin/', xadmin.site.urls),
    # TemplateView.as_view方法会自动返回一个view函数来简单的返回一个HTML静态页面
    # 如果要动态的显示html页面，那么view函数需要自己写
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    #  'login/'和'login'，有斜线的两种模式都可以访问
    # name参数用来代表‘login/’访问地址的别名，方便在html的其它位置使用
    path('login/', LoginView.as_view(), name='login'),
    path('d_login/', DynamicLoginView.as_view(), name='d_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),  # 图片动态验证码的路由，前端ajax访问

    # 配置上传文件的URL
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 机构相关的页面, 将所有与机构列表相关的以org开头的url都指向organizations app中的urls文件
    # 限定organizations.urls的命名空间为namespace='org'，在HTML中对organizations.urls的url的引用变为url 'org:具体url名称'
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),
]

# 1. CBV(class vase view)  FBV(function base view)

# 编写一个View的几个步骤：
# 1. view代码
# 2. 配置url
# 3. 修改HTML中相关的地址

