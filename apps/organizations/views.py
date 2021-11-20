from django.shortcuts import render
from django.views.generic.base import View

from apps.organizations.models import CourseOrg, City


class OrgView(View):
    # 重写get方法
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()  # 获取机构数据表
        org_nums = CourseOrg.objects.count()    # 统计总共有多少家机构
        all_citys = City.objects.all()  # 获取数据库中的所有城市
        return render(request, 'org-list.html', {
            'all_orgs': all_orgs,
            'org_nums': org_nums,
            'all_citys': all_citys,
        })
