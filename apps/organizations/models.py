from django.db import models

from apps.users.models import BaseModel


class City(BaseModel):
    """
    城市表
    """
    name = models.CharField(verbose_name='城市名称', max_length=50)
    desc = models.CharField(verbose_name='城市描述', max_length=200)

    def __str__(self):
        return self.name  # toString 城市名称

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name


class CourseOrg(BaseModel):
    """
    课程机构表
    """
    city = models.ForeignKey(City, verbose_name='所在城市', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='机构名称', max_length=50)
    desc = models.TextField(verbose_name='机构描述', default='')
    tag = models.CharField(verbose_name='机构标签', max_length=10, default='全国知名')
    category = models.CharField(verbose_name='机构类别', max_length=20,
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), default='pxjg')
    click_nums = models.IntegerField(verbose_name='点击数量', default=0)
    fav_name = models.IntegerField(verbose_name='收藏数', default=0)
    image = models.ImageField(verbose_name='logo', upload_to='org/%Y/%m', max_length=100)
    address = models.CharField(verbose_name='机构地址', max_length=150)
    students = models.IntegerField(verbose_name='学习人数', default=0)
    course_nums = models.IntegerField(verbose_name='课程数量', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name


class Teacher(BaseModel):
    """
    讲师表
    """
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='教师姓名', max_length=50)
    work_years = models.IntegerField(verbose_name='工作年限', default=0)
    work_company = models.CharField(verbose_name='就职单位', max_length=50)
    work_position = models.CharField(verbose_name='单位职位', max_length=50)
    points = models.CharField(verbose_name='教学特点', max_length=50)
    click_nums = models.IntegerField(verbose_name='点击次数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏次数', default=0)
    age = models.IntegerField(verbose_name='年龄', default=18)
    image = models.ImageField(verbose_name='头像', upload_to='teacher/5%Y/%m', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
