from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.courses'
    verbose_name = '课程管理'   # 用来在后台管理系统中显示的名称
