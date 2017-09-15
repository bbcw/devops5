from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse, Http404, HttpResponse
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


#class GroupListView(ListView):
# 添加登录验证
class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupCreateView(View):
    def post(self, request):

        # 在view中权限验证
        if not request.user.has_perm('auth.add_group'):
            return HttpResponse('Forbidden')

        ret = {"status": 0}
        group_name = request.POST.get("name", "")
        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)

class GroupUserList(TemplateView):
    template_name = "user/group_userlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)

        # 将指定用户组内的成员列表取出来传给模板

        # 通过request获取gid,并给一个为空的默认值
        gid = self.request.GET.get("gid", "")

        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist!")

        context['gid'] = gid
        return context

# 删除用户组
class GroupDeleteView(View):
    def post(self, request):
        print(request.POST)

        ret = {"status": 0}
        gid = request.POST.get("gid", "")
        group_obj = Group.objects.get(pk=gid)
        perm_count = group_obj.permissions.count()
        group_count = group_obj.user_set.all()
        if perm_count:
            ret['status'] = 1
            ret['errmsg'] = "用户组有权限，不能删除"
            return JsonResponse
        if group_count:
            ret['status'] = 1
            ret['errmsg'] = "用户组包含用户，不能删除"
            return JsonResponse
        try:
            g = Group(name=group_obj)
            g.delete()
        except IntegrityError:
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)

# 查看用户组权限
class ListGroupPermissionList(ListView):
    model = Permission
    template_name = "user/list_group_permissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 将指定用户组内的成员列表取出来传给模板
        # 通过request获取gid,并给一个为空的默认值
        gid = self.request.GET.get('gid', '')

        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.permissions.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist!")

        context['gid'] = gid
        print(context)
        return context

class ModifyGroupPermissionList(TemplateView):
    template_name = 'user/modify_group_permissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        context['group'] = self.request.GET.get('gid')
        context['group_permissions'] = self.get_group_permissions(context['group'])
        print(context)
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            # 返回用户组的权限id
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect('error', next='group_list', msg='用户组不存在')

    def post(self, request):

        # 在view中权限验证
        if not request.user.has_perm('auth.add_permission'):
            return HttpResponse('Forbidden')

        print(request.POST)
        permission_id_list = request.POST.getlist('permission', [])
        print(permission_id_list)
        groupid = request.POST.get('groupid', 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return redirect('error', next='group_list', errmsg='用户组不存在')

        if len(permission_id_list) > 0:
            permission_objs = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_objs)
        else:
            group_obj.permissions.clear()
        return redirect('success', next='group_list')
