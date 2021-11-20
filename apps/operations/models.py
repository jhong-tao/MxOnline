from django.db import models
from django.contrib.auth import get_user_model  # django中用从settings配置文件中的AUTH_USER_MODEL属性来获取用户表的类

from apps.users.models import BaseModel
from apps.courses.models import Course

# 由于目前我的settings.py中AUTH_USER_MODEL = 'users.UserProfile'，所以当前使用的用户表的类就是我自己定义的UserProfile
# 用了get_user_model方法，就可以不用在模块导入中导入UserProfile类了，而是从配置文件中去获取用户类
User = get_user_model()  # 这一句就类似于导入了 UserProfile，这样的目的是方便通过配置文件来设置用户类，方便以后修改用户类


class UserAsk(BaseModel):
    """
    用户咨询信息表
    """
    name = models.CharField(verbose_name='姓名', max_length=20)
    mobile = models.CharField(verbose_name='手机', max_length=11)
    course_name = models.CharField(verbose_name='课程名称', max_length=50)

    def __str__(self):
        return self.name +"-"+ self.course_name

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(BaseModel):
    """
    课程评论表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)

    comments = models.CharField(verbose_name='评论内容', max_length=200)

    def __str__(self):
        return self.user.name +"-"+ self.course.name

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel):
    """
    用户的收藏表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

    fav_id = models.IntegerField(verbose_name='数据id')
    fav_type = models.IntegerField(verbose_name='收藏类型', choices=((1, '课程'), (2, '课程机构'), (3, '讲师')), default=1)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(BaseModel):
    """
    用户的消息表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

    message = models.CharField(verbose_name='消息内容', max_length=200)
    has_read = models.BooleanField(verbose_name='是否已读', default=False)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(BaseModel):
    """
    用户与课程关系的表 n-n
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name +"-"+ self.course.name

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
