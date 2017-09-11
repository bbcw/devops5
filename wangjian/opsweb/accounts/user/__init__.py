from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import reverse
from django.conf import settings

class UserListView(LoginRequiredMixin,ListView):
    """用户展示视图"""
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8         # 每页展示多少对象
    before_range_num = 4    # 当前页往前几页
    after_range_num = 4     # 当前页往后几页
    ordering = "id"


    def get_queryset(self):
        """
        用户列表搜索框搜索条件后端从数据库取出数据的逻辑
        查询数据库，获得查询对象的集合，list，其中每个元素对应数据表里的一条记录
        """
        queryset = super(UserListView, self).get_queryset()
        queryset = queryset.filter(is_superuser=False)              # 过滤掉有 is_superuser  属性的用户

        username = self.request.GET.get("search_username", None)    # 查询前端传递的 username
        if username:
            queryset = queryset.filter(username__icontains=username) #按照前端传递的 username 进行查询

        return queryset

    def get_context_data(self, **kwargs):
        """用户列表搜索后的数据展示给前端"""
        context = super(UserListView, self).get_context_data(**kwargs)  # 覆盖父类的属性

        # 当前页  的前7条
        """
        current_index = context['page_obj'].number
        start = current_index - 3
        end = current_index + 3
        if start <= 0:
            start = 1
        if end > context['paginator'].num_pages:
            end = context['paginator'].num_pages
        context['page_range'] = range(start, end)
        """
        context['page_range'] = self.get_pagerange(context['page_obj'])
        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        """
        用户列表分页逻辑/accouts/user/list/
        page_obj 是需要传递的参数，为当前页的模型对象，可以遍历获得该对象里的内容
        """
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end+1)

    #@method_decorator(permission_required("auth.add_user", login_url=reverse("error",kwargs={"next":"dashboard", "msg":"没有权限，请联系管理员"})))
    @method_decorator(permission_required("auth.add_user",login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)

class ModifyUserStatusView(View):
    """
    用户列表页面中修改用户状态(禁用和正常)的逻辑
    响应前端 ajax 请求修改用户状态
    """
    def post(self, request):
        uid = request.POST.get("uid", "")
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


class ModifyUserGroupView(View):
    """修改用户和组关系的逻辑"""
    def get(self, request):
        """展示用户列表"""
        print(request.GET)
        uid = request.GET.get('uid', "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        """将用户添加到用户组逻辑"""
        ret = {"status":0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] =1
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
        """
        """
        ret = {"status": 0}
        data = QueryDict(request.body)
        try:
            user_obj = User.objects.get(id=data.get('uid', ""))
            group_obj = Group.objects.get(id=data.get('gid', ""))
            user_obj.groups.remove(group_obj)

            #group_obj.user_set.remove(user_obj)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        return JsonResponse(ret)

