# Generated by Django 3.2.9 on 2021-11-14 04:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加实体')),
                ('name', models.CharField(max_length=50, verbose_name='城市')),
                ('desc', models.CharField(max_length=200, verbose_name='城市描述')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加实体')),
                ('name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('desc', models.TextField(default='', verbose_name='机构描述')),
                ('tag', models.CharField(default='全国知名', max_length=10, verbose_name='机构标签')),
                ('category', models.CharField(choices=[('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')], default='pxjg', max_length=20, verbose_name='机构类别')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数量')),
                ('fav_name', models.IntegerField(default=0, verbose_name='收藏数')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='logo')),
                ('address', models.CharField(max_length=150, verbose_name='课程地址')),
                ('students', models.IntegerField(default=0, verbose_name='学习人数')),
                ('course_nums', models.IntegerField(default=0, verbose_name='课程数量')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.city', verbose_name='所在城市')),
            ],
            options={
                'verbose_name': '课程机构',
                'verbose_name_plural': '课程机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加实体')),
                ('name', models.CharField(max_length=50, verbose_name='教师姓名')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('work_company', models.CharField(max_length=50, verbose_name='就职单位')),
                ('work_position', models.CharField(max_length=50, verbose_name='单位职位')),
                ('points', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击次数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏次数')),
                ('age', models.IntegerField(default=18, verbose_name='年龄')),
                ('image', models.ImageField(upload_to='teacher/5%Y/%m', verbose_name='头像')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.courseorg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
    ]
