import math

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from apps.organizations.models import CourseOrg, City
from apps.organizations.forms import AddAskForm


class OrgCourseView(View):
    """
    OrgCourseView 用来显示机构下的课程页面的请求
    """
    # 重写get方法
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'course'
        course_org: CourseOrg = CourseOrg.objects.get(id=int(org_id))  # 通过课程机构的id获取课程机构
        course_org.click_nums += 1  # 课程机构点击次数增加1
        course_org.save()

        all_courses = course_org.course_set.all()  # 获取机构下面的所有课程
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    """
    OrgTeacherView 用来显示机构下面的教师的请求
    """
    # 重写get方法
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'teacher'
        course_org: CourseOrg = CourseOrg.objects.get(id=int(org_id))  # 通过课程机构的id获取课程机构
        course_org.click_nums += 1  # 课程机构点击次数增加1
        course_org.save()

        all_teacher = course_org.teacher_set.all()  # 获取机构下面的所有老师
        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgHomeView(View):
    """
    OrgHomeView 用来处理机构首页的请求
    """
    # 重载get方法
    def get(self, request, org_id, *args, **kwargs):
        current_page = 'home'   # 传递个前端用来判断当前侧边栏选择的是哪个选项
        course_org: CourseOrg = CourseOrg.objects.get(id=int(org_id))  # 通过课程机构的id获取课程机构
        course_org.click_nums += 1  # 课程机构点击次数增加1
        course_org.save()

        all_courses = course_org.course_set.all()[:3] # 获取课程机构的前三个课程
        all_teacher = course_org.teacher_set.all()[:1]  # # 获取课程机构的前一个讲师
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
        })


class AddAskView(View):
    """
    AddAskView:处理用户在机构列表页的咨询
    """
    # 重载post方法
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            # 如果表单数据验证通过，直接保存到数据库,commit=True表示直接提交到数据库
            user_ask = userask_form.save(commit=True)  # 返回值为UserAsk实例
            return JsonResponse({
                'status': 'success',
                'msg': '留言成功'
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '留言失败'
            })


class OrgView(View):
    """
    OrgView:用来显示课程机构列表页
    """
    # 重写get方法
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()  # 获取机构数据表
        all_citys = City.objects.all()  # 获取数据库中的所有城市

        # 授课机构排名
        hot_orgs = all_orgs.order_by('click_nums')[:3]  # 根据点击数排名,取前三名

        # 通过机构类别对课程机构进行筛选
        category = request.GET.get('ct', '')  # 获取前端选择的机构类别
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过地区对机构进行筛选
        city_id = request.GET.get('city', '')  # 获取前端选择的城市
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))  # django 提供了可以直接通过外键访问关联表

        org_nums = all_orgs.count()  # 统计总共有多少家机构

        # 对筛选过后的机构进行排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')  # -students 按照学习人数倒数排序
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')  # -course_nums 按照课程数量倒数排序

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 分页操作，每页显示5条记录
        p = Paginator(object_list=all_orgs, per_page=5, request=request)
        orgs = p.page(page)  # orgs为page对象，通过他的orgs.object_list方法获取querySet对象

        return render(request, 'org-list.html', {
            'all_orgs': orgs,  # 传递分页之后的机构数据表对象到前端html
            'org_nums': org_nums,
            'all_citys': all_citys,
            'category': category,  # 传递类别到前端，用来做样式设置判断
            'city_id': city_id,  # city_id传递到前端用来判断选择哪个城市
            'sort': sort,  # 将排序规则传递到前端
            'hot_orgs': hot_orgs  # 授课机构排名
        })
