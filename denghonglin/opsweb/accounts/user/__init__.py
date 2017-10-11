from django.views.generic import ListView,View
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import reverse
from django.conf import settings

# 导入自定义模块
from accounts.models import Profile

class UserListView(LoginRequiredMixin,ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 4
    ordering = 'id'

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        #queryset = queryset.exclude(username="admin")
        queryset = queryset.filter(is_superuser=False)

        username = self.request.GET.get("search_username",None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView,self).get_context_data(**kwargs)
        
        # 当前页的前7页
        """
        curent_index = context['page_obj'].number
        start = curent_index - 4
        end = curent_index + 4

        if start <= 0:
            start = 1
        if end > context['paginator'].num_pages:
            end = context['paginator'].num_pages
       
        context['page_range'] = range(start,end)
        """

        context['page_range'] = self.get_pagerange(context['page_obj'])

        #处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num

        if start <= 0:
            start = 1
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end)

    #@method_decorator(permission_required("auth.add_user",login_url=reverse("error",kwargs={"next":"dashboard","msg":"没有权限，请联系管理员"})))
    @method_decorator(permission_required("auth.add_user",login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(UserListView,self).get(request, *args, **kwargs)

    def post(self,request):
        username = request.POST.get('username','')
        name = request.POST.get('name','')
        phone = request.POST.get('phone','')
        # weixin = request.POST.get('weixin','')
        email = request.POST.get('email','')
        # print(username,name,phone,email)

        try:
            user = Profile()
            user.username = username
            user.name = name
            user.phone = phone
            # user.weixin = weixin
            user.email = email
            user.password = make_password("123456")
            user.is_active = True
            user.save()

            ret = {'status':0,'result':'{0}用户添加成功'.format(name)}

        except:
            ret = {'status':1,'errmsg':'添加用户失败'}
        return JsonResponse(ret,safe=True)
            

class ModifyUserStatusView(LoginRequiredMixin,View):
    def post(self, request):
        uid = request.POST.get("uid","")
        ret = {"status":0}
        try:
            user_obj = User.objects.get(id=uid)
            #user_obj.is_active = False if user_obj.is_active else True
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True   
            user_obj.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
            
        return JsonResponse(ret)

class ModifyUserGroupView(LoginRequiredMixin,View):
    
    def get(self,request):
        uid = request.GET.get('uid',"")
        group_objs = Group.objects.all()

        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_objs.values("id","name")),safe=False)

    def put(self,request):
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get("uid","")
        gid = data.get("gid","")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status":0}
        data = QueryDict(request.body)
        try:
            user_obj = User.objects.get(id=data.get('uid',""))
            group_obj = Group.objects.get(id=data.get('gid',""))
            # 以下两种方式任选一种使用。
            user_obj.groups.remove(group_obj)  
            #group_obj.user_set.remove(user_obj) 
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        return JsonResponse(ret)

class GetUserListView(View):
    def get(self, request):
        users = User.objects.values("id","email","username")
        return JsonResponse(list(users),safe=False)
