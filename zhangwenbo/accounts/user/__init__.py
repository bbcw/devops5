from django.views.generic import ListView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from django.http import JsonResponse, QueryDict
from accounts.models import Profile

class UserListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = "auth.view_user"
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 5
    ordering = "id"


    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        queryset = queryset.filter(is_superuser=False)

        username = self.request.GET.get("search_username", None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])

        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        if search_data:
            context["search_data"] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end+1)


class ModifyUserStatusView(LoginRequiredMixin,View):

    def post(self, request):
        uid = request.POST.get("uid", "")
        ret = {"status":0}
        if not request.user.has_perm('auth.change_user'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        try:
            user_obj = User.objects.get(id=uid)
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            user_obj.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        return JsonResponse(ret)


class ModifyUserGroupView(LoginRequiredMixin, View):
    def get(self, request):
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
        ret = {"status":0}
        if not request.user.has_perm('auth.add_group'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
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
        if not request.user.has_perm('auth.delete_user'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        data_name = QueryDict(request.body)
        username = data_name.get("username", "")
        groupname = data_name.get("groupname", "")
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(name=groupname)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)
        user_obj.groups.remove(group_obj)
        return JsonResponse(ret)
