from django.db import models
from django.contrib.auth.models import AbstractUser  # 导入django的用户类，继承他来创建我们自己的用户类(用户表)

# 通过定义一个元组用来给性别做选择
GENDER_CHOICES = (
    ('male', '男'),  # 在数据库中存入的是male,显示用的男
    ('female', '女')
)


# 创建自己的用户类
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')  # 用户昵称，默认为空字符串
    # 如果要设置一个字符串类型的值可以为空，一般用空字符串""表示,默认blank=false，表示输入不能为空
    # 如果对于日期，数字等类型的值允许为空时，需要同时设置null=True, blank=True
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)  # 生日，允许为空
    gender = models.CharField(verbose_name='性别', choices=GENDER_CHOICES, max_length=6)  # choices用来限制可输入的值
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')  # unique=True表示该字段不能重复
    # ImageField实际上保存的是图片的路径,通过media中的默认图片作为用户的头像
    image = models.ImageField(upload_to='head_image/%Y%m', default='default.jpg', verbose_name='用户头像')

    # Meta用来描述UserProfile的名称和信息

    class Meta:
        # db_table = '用户信息' # db_table指定了对应的表明；而表明默认为app名 + 类名： [app_name]
        verbose_name = '用户信息'  # verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示
        verbose_name_plural = verbose_name  # verbose_name_plural表示复数形式的显示；

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username  # toString返回用户名
