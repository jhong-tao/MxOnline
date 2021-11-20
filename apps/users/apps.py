from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'     # 配置app的名称，该名称在settings文件中配置后，会用users来表示当前的APP
    verbose_name = '用户管理'     # verbose_name属性用来设置APP名称在后台管理系统中显示的名字，不设置则后台显示的名称为users
