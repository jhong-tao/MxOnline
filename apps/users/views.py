from django.shortcuts import render
from django.views.generic.base import View  # CBV,所有的View类都要继承这个View
# authenticate django提供的用来判断用户是否存在的方法,login方法中包含了cookie和session的机制,logout则是实现退出功能
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse # HttpResponseRedirect 这个方法用来重定向网页,JsonResponse返回json
from django.urls import reverse  # reverse函数用来通过urls文件中配置的url别名去找到真正的url
import redis

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm  # 用来做表单验证
from apps.users.forms import RegisterGetForm, RegisterPostForm # 注册手机短信验证码表单验证
from apps.utils.YunPian import send_single_sms  # send_single_sms 用来发送短信验证码
from MxOnline.settings import yp_apikey # 云片网的apikey
from apps.utils.random_str import generate_random
from apps.utils.db_utils import redis_set
from apps.users.models import UserProfile
"""

"""

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()   # 实例化注册短信验证码表单验证对象，传递图片验证码
        return render(request, 'register.html', {
            'register_get_form': register_get_form})  # register_get_form.captcha 传递图片验证码到注册页面

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm()  # 表单数据验证，包括图片验证码验证
        # 验证通过，新建用户
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data['mobile']
            password = register_post_form.cleaned_data['password']
            user = UserProfile(username=mobile, mobile=mobile)  # 默认设置用户的姓名和手机号相同
            user.set_password(password)  # user.set_password方法会将明文的密码自动加密
            user.save()  # 将新建的用户保存到数据库
            login(request, user)  # 注册成功，登录
            return HttpResponseRedirect(reverse('index'))  # 登录成功，跳转到首页
        else:
            # 验证没通过，则回填数据，返回注册页面
            register_post_form = RegisterPostForm()
            return render(request, 'login.html', {
                'register_post_form': register_post_form
            })


class DynamicLoginView(View):
    """
    DynamicLoginView 动态短信验证码登录视图类

    """
    # 重载post方法，因为前端获取短信验证码的ajax用的是post方法
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)  # DynamicLoginPostForm已经完成图片验证码的验证
        dynamic_login = True  # dynamic_login用来在前端判断当前是普通登录还是动态登录
        # #表单验证结果判断
        if login_form.is_valid():
            # 没有注册过的手机号码也能登录，这个时候就完成了注册加登录的功能
            mobile = login_form.cleaned_data['mobile']  # 获取用户的手机号码
            existed_users = UserProfile.objects.filter(mobile=mobile)  # 根据手机号查询用户是否存在
            # 如果用户存在，则进行登录，否则就是注册+登录
            if existed_users:
                user = existed_users[0]
            else:  # 用户不存在则注册加登录
                # 新建用户
                user = UserProfile(username=mobile, mobile=mobile)  # 默认设置用户的姓名和手机号相同
                password = generate_random(10, 2)  # 给用户生成随机的明文密码
                user.set_password(password)  # user.set_password方法会将明文的密码自动加密
                user.save()  # 将新建的用户保存到数据库
            login(request, user)  # 登录
            return HttpResponseRedirect(reverse('index'))  # 登录成功，跳转到首页
        else:
            # 如果前端数据校验没通过
            d_form = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form,
                                                  'd_form': d_form,  # 图片验证码信息
                                                  'dynamic_login': dynamic_login})


class SendSmsView(View):
    """
    sendSmsView，发送短信验证码的处理类，用来处理前端ajax请求的短信验证
    """

    # 重载post方法，因为前端获取短信验证码的ajax用的是post方法
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)  # 获取前端传递过来的图片动态验证码
        re_dict = {}  # 返回给前端ajax的信息
        # 判断ajax提交的图片验证码和电话号码数据是否合法
        if send_sms_form.is_valid():
            # 图片验证码正确，进行手机验证码验证
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4, 0)  # 生成4位随机数
            re_json = send_single_sms(yp_apikey, code=code,mobile=mobile)
            if re_json['code'] == 0:
                # 短信发送成功
                re_dict['status'] = 'success'
                # 短信验证码发送成功，则需要在服务器本地内存中存放该验证码，用来与前端输入的验证码做校验
                redis_set(mobile, code, 5)
            else:  # 短信发送失败
                re_dict['msg'] = re_json['msg']
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LoginView(View):
    """
    LoginView:登录验证
    """

    # 重载View的get方法，处理get请求, 必须接收一个request参数，django自动注入的request请求
    def get(self, request, *args, **kwargs):
        # render django 内置的用来渲染html的渲染器，渲染好了之后返回给浏览器
        # render 必须包含request参数和需要被渲染的html页面
        # 用户点击登录按钮的时候先来判断用户当前是否已经登录,用这个属性来判断用户的登录状态
        # 如果用户登录了request中的user对象会是一个实例，没有登录则是一个匿名对象
        if request.user.is_authenticated:
            # 如果用户已经登录，则自动重定向到首页
            return HttpResponseRedirect(reverse('index'))
        # 没有登录则进入登录页面
        login_form = DynamicLoginForm()  # 通过captcha，DynamicLoginForm实现图片动态验证码验证
        return render(request, 'login.html', {
            'login_form': login_form  # 返回图片验证码
        })

    # 重载post方法
    def post(self, request, *args, **kwargs):
        # 前端form表单数据验证,用继承django提供的表单验证的类LoginForm实现表单验证
        login_form = LoginForm(request.POST)  # 实例化LoginForm，必须传递request.POST参数，才能获取前端的数据
        # 调用is_valid方法验证前端数据的合法性
        if login_form.is_valid():
            # 如果前端form表单的数据校验通过，则需要去数据库查询用户是否存在，完成登录
            # 使用login_form对象的cleaned_data方法获取前端form通过request.POST传递过来的值，cleaned_data返回的是字典类型
            username = login_form.cleaned_data['username']  # username 必须是与前端的name属性值一致
            password = login_form.cleaned_data['password']
            # 使用django提供的用户是否存在于数据中的查询方法authenticate，验证用户是否存在
            user = authenticate(username=username, password=password)  # authenticate 方法需要传递用户名和密码
            if user is not None:
                # 查询到用户存在
                # login是django提供的登录函数，需要传递request和user两个参数，登录后悔自动创建cookies和session
                login(request, user)
                # 登录成功后怎么返回页面
                # return render(request, 'index.html')    #         # render 返回的页面不会修改浏览的地址
                return HttpResponseRedirect(reverse('index'))  # reverse函数用来通过urls中配置的url别名去找到真正的url
            else:
                # 查询不到用户，应该给一些提示,并把用户错误的数据显示回表单
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            # 如果前端数据校验没通过
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    # 重载View的get方法
    def get(self, request, *args, **kwargs):
        # logout方法是django提供的退出方法，需要传递request对象
        logout(request)
        return HttpResponseRedirect(reverse('index'))  # 退出后重定向到首页

