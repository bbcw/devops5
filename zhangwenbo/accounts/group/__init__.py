from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse, Http404, HttpResponse, QueryDict
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import CreateGroupForm
from accounts.mixins import PermissionRequiredMixin

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    '''
    用户组列表
    '''
    permission_required = "auth.view_group"
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {"status": 0}
        if not request.user.has_perm('auth.add_group'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        groupform = CreateGroupForm(request.POST)
        if groupform.is_valid():
            try:
                g = Group(**groupform.cleaned_data)
                g.save()
            except Exception as e:
                ret['status'] = 1
                ret['errmsg'] = e.args
        else:
            ret['status'] = 1
            ret['errmsg'] = "输入无效内容"
        return JsonResponse(ret)

        # '''
        # group_name = request.POST.get("name", "")
        # if not group_name:
        #     ret['status'] = 1
        #     ret['errmsg'] = "用户组不能为空"
        #     return JsonResponse(ret)
        # try:
        #     g = Group(name=group_name)
        #     g.save()
        # except IntegrityError:
        #     ret['status'] = 1
        #     ret['errmsg'] = "用户组已存在"
        # return JsonResponse(ret)
        # '''

class GroupDeleteView(LoginRequiredMixin, View):
    def delete(self, request):
        ret = {"status":0}
        if not request.user.has_perm('auth.delete_group'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        data_name = QueryDict(request.body)
        groupid = data_name.get("gname", "")
        try:
            g = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)
        try:
            gtou = g.user_set.all()
            if gtou:
                ret['status'] = 1
                ret['errmsg'] = "该组有用户，不能删除"
                return JsonResponse(ret)
        except:
            pass
        try:
            gtoper = g.permissions.all()
            if gtoper:
                ret['status'] = 1
                ret['errmsg'] = "该组有组权限，不能删除"
                return JsonResponse(ret)
        except:
            pass
        g.delete()
        return JsonResponse(ret)

class GroupuserListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "auth.view_user"

    def get(self, request, *args, **kwargs):
        groupid = request.GET.get("gid", "")
        try:
            get_group = Group.objects.get(id=groupid)
            object_list = get_group.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group is not exist.")
        return render(request, "user/groupuserlist.html", {"object_list": object_list, "groupname":get_group})

class ModifyGroupPermissionList(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.change_permission"
    template_name = "user/modify_group_permission.html"

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

class GroupPermissionListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "auth.view_permission"
    template_name = "user/permission_group_list.html"

    def get_context_data(self, **kwargs):
        context = super(GroupPermissionListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(pk=gid)
            context["groupname"] = group_obj
            context["group_permissions"] = group_obj.permissions.all()
            return context
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")