from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import  View,TemplateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import myPermissionRequiredMixin

# Create your views here.
# -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  login----------------
'''

def login_view(request):
    if request.method == "GET":
        return render(request, "public/login.html")
    else:
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)
'''


'''
# view 登录验证
class Login_View(View):

    def get(self,request,*args,**kwargs):
        return render(request, "public/login.html")
    

    def post(self,request,*args,**kwargs):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)
'''



'''
TemplateView  的 template_name 指定 get 方法的模版名称
所以这个属性和 post 等其他属性无关
若有 其他方法还是要 自己去写相应的函数的。
'''
class LoginView(TemplateView):
    template_name = 'public/login.html'

    def get(self,request,*args,**kwargs):
        return  super(LoginView, self).get(request,*args,**kwargs)


    def post(self,request,*args,**kwargs):
        username = request.POST.get("username", "")
        userpass = request.POST.get("password", "")
        user = authenticate(username=username, password=userpass)
        ret = {"status":0, "errmsg":""}
        if user:
            login(request, user)
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
            ret['errmsg'] = "用户名或密码错误，请联系管理员"
        return JsonResponse(ret)


 # -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  logout----------------

'''
#普通函数方法
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))
    
    
# class view 实现退出
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  HttpResponseRedirect(reverse("user_login"))
'''

#templateview 实现退出
class LogoutView(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  HttpResponseRedirect(reverse("user_login"))




# -------------  以下为   函数视图  view类视图  templateview 类视图  三种方法 实现  user_list----------------
@login_required
def user_list_view(request):
    user_queryset = User.objects.all()
    for user in user_queryset:
        print(user.username, user.email)
    return render(request, "user/userlist.html", {"userlist":user_queryset })

'''
class UserListView(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        user_queryset = User.objects.all()
        return render(request, "user/userlist.html", {"userlist": user_queryset})
'''




'''
#---------------------------------------------------原始方法分页练习-------------------------------
class UserListView(TemplateView):
    template_name = 'user/userlist.html'
    per = 10

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs )
        try:
            page =  int(self.request.GET.get("page",1))
            print(page)
        except:
            page = 1

        start = (page - 1) * self.per
        end = page * self.per
        print(end ,start)
        context['userlist']=User.objects.all()[start:end]
        return context

'''
'''
#---------------------------------------------------paginator  方法分页练习-------------------------------

class UserListView(LoginRequiredMixin,TemplateView):
    template_name = 'user/userlist.html'
    per = 5
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserListView, self).get_context_data(**kwargs )
        try:
            page_num =  int(self.request.GET.get("page",1))
        except:
            page_num = 1

        user_list =  User.objects.all().filter(is_superuser=False)
        paginator = Paginator(user_list,self.per)
        zong = paginator.num_pages
        if page_num > zong:
            page_num = zong
        if page_num < 0:
            page_num = 1

        context['page_obj'] =  paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list

        current_page = context['page_obj'].number-1
        startpage = current_page - 4
        endpage = current_page + 5

        sdiffpage = 0
        ediffpage = 0

        if startpage < 0 :
            sdiffpage = -startpage

        if endpage > zong:
            ediffpage = endpage - zong

        endpage += sdiffpage
        startpage -= ediffpage

        if endpage > zong:
            endpage = zong
        if startpage < 0:
            startpage =0

        print(startpage,endpage)
        # if zong > showpage or zong<showpage:
        context['page_range'] = paginator.page_range[startpage:endpage]
        return context
'''


class UserListView(LoginRequiredMixin,myPermissionRequiredMixin,ListView):
    permission_required = 'auth.view_user'
    msg = '您没有查看用户列表的权限，请联系管理员。'

    paginate_by  = 5
    template_name = "user/userlist.html"
    model = User
    ordering = 'id'


    # @method_decorator(permission_required("auth.add_user",login_url='/dashboard/error/dashboard/你没有权限'))
    # def get(self, request, *args, **kwargs):
    #     return  super(UserListView, self).get(request, *args, **kwargs)


    def get_queryset(self):
        querset = super(UserListView, self).get_queryset()
        querset = querset.filter(is_superuser = False)

        #处理搜索条件
        username = self.request.GET.get("search_username","")
        if username:
            querset = querset.filter(username__icontains=username)
        # print(username)
        return  querset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1

        user_list =  self.get_queryset()

        changdu = {"allnums":len(user_list)}
        context.update(changdu)
        paginator = Paginator(user_list, self.paginate_by)
        zong = paginator.num_pages
        if page_num > zong:
            page_num = zong
        if page_num < 0:
            page_num = 1

        context['page_obj'] = paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list

        current_page = context['page_obj'].number-1
        startpage = current_page - 4
        endpage = current_page + 5

        sdiffpage = 0
        ediffpage = 0

        if startpage < 0:
            sdiffpage = -startpage

        if endpage > zong:
            ediffpage = endpage - zong

        endpage += sdiffpage
        startpage -= ediffpage

        if endpage > zong:
            endpage = zong
        if startpage < 0:
            startpage = 0

        # print(startpage, endpage)
        context['page_range'] = context['paginator'].page_range[startpage:endpage]

        #处理搜索条件
        search_data = self.request.GET.copy()
        search_data = search_data.dict().get('search_username',"")
        print(search_data)

        if search_data:
            context['search_word'] = search_data
            context['search_username']="&search_username="+search_data

        return  context


