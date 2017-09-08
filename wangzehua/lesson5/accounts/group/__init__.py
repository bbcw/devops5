from django.views.generic import View, ListView, CreateView, TemplateView
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse, Http404, QueryDict
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
#from accounts.views import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "user/grouplist.html"
    model = Group
    ordering = "id"
    permission_required = "auth.add_group"
    permission_redirect_field_name = "index"

    '''
    @method_decorator(permission_required("auth.add_group", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(GroupListView, self).get(request, *args, **kwargs)
    '''

class GroupUserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = "user/groupuserlist.html"
    permission_required = "auth.change_group"
    permission_redirect_field_name = "index"

    def get_queryset(self):
        print(self.request.GET)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            #User.objects.all().filter(=gid)
        except Group.DoesNotExist:
            pass
        else:
            user_objs = group_obj.user_set.all()
        queryset = user_objs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            pass
        else:
            context["group_obj"] = group_obj
        return context

    '''
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_group", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(GroupUserListView, self).get(request, *args, **kwargs)
    '''

class GroupUserList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "user/groupuserlist.html"
    permission_required = "auth.change_group"
    permission_redirect_field_name = "index"

    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist")
        #except Group.MultipleObjectsReturned

        return context

    '''
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_group", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(GroupUserList, self).get(request, *args, **kwargs)
    '''
'''
class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "auth.add_group"
    permission_redirect_field_name = "index"

    def post(self, request):
        ret = {"status":0}
        groupname = request.POST.get("name", "")
        if not groupname:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        print(request.POST)
        try:
            """
            g = Group()
            g.name = groupname
            g.save()
            """
            g = Group(name=groupname)
            g.save()
        except IntegrityError as e:
            print("IntegrityError")
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)
'''

class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "auth.add_group"
    permission_redirect_field_name = "index"

    def post(self, request):
        ret = {"status":0}
        groupname = request.POST.get("name", "")
        if not groupname:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        print(request.POST)
        try:
            """
            g = Group()
            g.name = groupname
            g.save()
            """
            g = Group(name=groupname)
            g.save()
        except IntegrityError as e:
            print("IntegrityError")
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"

        return JsonResponse(ret)

    '''
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_group", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(GroupCreateView, self).get(request, *args, **kwargs)
    '''

class ModifyGroupPermissionList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "user/modify_group_permissions.html"
    permission_required = "auth.change_group"
    permission_redirect_field_name = "index"

    def get_context_data(self, **kwargs):
            context = super(ModifyGroupPermissionList, self).get_context_data(**kwargs)
            context["contenttypes"] = ContentType.objects.all()
            context["group"] = self.request.GET.get("gid")
            context["group_permissions"] = self.get_group_permissions(context["group"])
            return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

    def post(self, request):
        print(request.POST)
        permission_id_list = request.POST.getlist("permission", [])
        groupid = request.POST.get("groupid", 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

        if len(permission_id_list) > 0:
            permission_objs = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_objs)
        else:
            group_obj.permissions.clear()
        return redirect("success", next="group_list")

class GroupPermissionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "user/group_permissionlist.html"
    model = Permission
    paginate_by = 10
    ordering = "id"
    permission_required = "auth.add_group"
    permission_redirect_field_name = "index"

    def get_queryset(self):
        print(self.request.GET)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            #User.objects.all().filter(=gid)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")
        else:
            group_permission_objs = group_obj.permissions.all()
        queryset = group_permission_objs
        return queryset

#homework 5
class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "auth.delete_group"
    permission_redirect_field_name = "group_list"

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)#通过form表单传，在body体里
        gid = data.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        if group_obj.user_set.count() > 0:
            ret['status'] = 1
            ret['errmsg'] = "用户组内存在用户"
        elif group_obj.permissions.count() > 0:
            ret['status'] = 1
            ret['errmsg'] = "用户组内存在权限设置"
        else:
            Group.delete(group_obj)
        return JsonResponse(ret)

