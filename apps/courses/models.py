from django.db import models  # django的models类

from apps.users.models import BaseModel  # 自定义的类，默认有添加资源的时间属性
from apps.organizations.models import Teacher

"""
在app的模型设计的时候，首先需要确定有哪些实体，然后确定出实体的属性和实体之间的关系
1. courses APP中实体类型：
Course-课程基本信息
Lesson-章节信息
Video-视频
CourseResource-课程资源
2. 关系
Course<1-n>Lesson
Lesson<1-n>Video
Course<1-n>CourseResource
Course<1-1>Teacher
3. 每一个实体的具体字段，也就是属性
    3.1 确定每一个字段的类型，是否是必填项, 也就是，属性名称，属性值类型，是否有默认值
4. 在3已经设计好表的基本属性之后，在来设计表直接的依赖关系，来设计外键    
"""


class Course(BaseModel):
    """
    课程表
    """
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='课程名称', max_length=50)
    desc = models.CharField(verbose_name='课程描述', max_length=300)
    learn_times = models.IntegerField(verbose_name='学习时长(分钟数)', default=0)
    degree = models.CharField(verbose_name='难度', max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')))
    students = models.IntegerField(verbose_name='学习人数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    click_nums = models.IntegerField(verbose_name='点击次数', default=0)
    category = models.CharField(verbose_name='课程类别', max_length=20, default='后端开发')
    tag = models.CharField(verbose_name='课程标签', max_length=10, default='')
    youneed_know = models.CharField(verbose_name='课程须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name='老师告诉你', max_length=300, default='')
    detail = models.TextField(verbose_name='课程详情', default='')
    image = models.ImageField('课程封面', upload_to='courses/%Y/%m', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class Lesson(BaseModel):
    """
    课程章节表
    """
    # on_delete表示当数据对应的外键被删除后，当前数据要不要跟着删除,CASCADE级联删除,置空SET_NULL，都不要调用，传递函数名即可，当实例化的时候
    # django会自动调用（），当设置置空SET_NULL时，一定要加上null=True,blank=True
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)  # 设置章节的外键，也就是章节属于那个课程

    name = models.CharField(verbose_name='章节名称', max_length=100)
    learn_times = models.IntegerField(verbose_name='学习时长(分钟数)', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name


class Video(BaseModel):
    """
    视频表
    """
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)  # 外键，必须放在第一个参数位置

    name = models.CharField(verbose_name='视频名称', max_length=100)
    learn_tiems = models.IntegerField(verbose_name='学习时长(分钟数)', default=0)
    url = models.CharField(verbose_name='访问地址', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程视频'
        verbose_name_plural = verbose_name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='资源名称', max_length=100)
    file = models.FileField(verbose_name='下载地址', upload_to='course/resourse/%Y/%m', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
