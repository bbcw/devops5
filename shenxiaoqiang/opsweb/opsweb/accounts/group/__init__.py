from django.contrib.auth.models import Group, ContentType, Permission
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse, HttpResponse, Http404, QueryDict
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from accounts.mixins import PermissionRequiredMixin

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "user/grouplist.html"

class GroupCreateView(LoginRequiredMixin, View):

    def post(self, request):
        ret = {"status":0}
        group_name = request.POST.get("name","")
        if not group_name:
            ret["status"] = 1
            ret["errmsg"] = "Group name is Null!!!"

        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError as e:
            # ret["status"] = 1
            # ret["errmsg"] = "用户组已存在!!!"
            return redirect("error", next="group_list", msg="Group is not exist!")
        return JsonResponse(ret)

    @method_decorator(permission_required("auth.add_group", login_url="group_list"))
    def get(self, request, *args, **kwargs):
        return super(GroupCreateView, self).get(request, *args, **kwargs)

class GroupUserListView(LoginRequiredMixin, TemplateView):
    template_name = "user/groupuserlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            g = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            raise Http404("page does not exist!!!")

        users = g.user_set.all()
        context['group_user_list'] = list(users.values("id", "username", "email"))
        context['gid'] = gid
        return context



class ModifyGroupListView(LoginRequiredMixin, View):

    def delete(self, request):
        ret = {
            "status": 0,
        }
        data = QueryDict(request.body)
        gid = data.get("gid", "")

        try:
            group_obj = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "Group is not exist!"

        group_user_check = group_obj.user_set.all()
        group_permission_check = group_obj.permissions.all()

        if group_user_check or group_permission_check:
            ret["status"] = 1
            ret["errmsg"] = "Delete Error! Groups or permissions are not empty!!!"
        else:
            Group.objects.filter(name__icontains=group_obj).delete()
        return JsonResponse(ret)


    @method_decorator(permission_required("auth.delete_group", login_url="group_list"))
    def get(self, request, *args, **kwargs):
        return super(ModifyGroupListView, self).get(request, *args, **kwargs)

class ModifyGroupPermissionListView(LoginRequiredMixin, TemplateView):
    template_name = "user/modify_group_permissions.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionListView, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        context["group"] = self.request.GET.get("gid", "")
        context["group_permissions"] = self.get_group_permissions(context["group"])
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="user group not exist!!!")

    def post(self, request):
        permission_id_list = request.POST.getlist("permission", [])
        groupid = request.POST.get("groupid", 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="user group not exist!!!")
        
        if len(permission_id_list) > 0:
            permission_obj = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_obj)
        else:
            group_obj.permissions.clear()
            
        return redirect("success", next="group_list")

    def delete(self, request):
        ret = {
            "status": 0,
        }
        data = QueryDict(request.body)
        pcodename = data.get("pcodename", "")
        gid = data.get("gid", "")

        try:
            group_obj = Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "Group is not exist!"

        try:
            permission_obj = Permission.objects.get(codename=pcodename)
        except Permission.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "Permission is not exist!"

        ## 通过用户组删权限
        group_obj.permissions.remove(permission_obj)
        
        return JsonResponse(ret)

    @method_decorator(permission_required("permission.delete_permission", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(ModifyGroupPermissionListView, self).get(request, *args, **kwargs)



class GroupPermissionListView(LoginRequiredMixin, ListView):
    template_name = "user/group_permissions_list.html"
    model = Permission
    paginate_by = 10
    ordering = "id"

    def get_queryset(self):
        queryset = super(GroupPermissionListView, self).get_queryset()
        group_id = self.request.GET.get("gid", "")

        if not group_id:
            return redirect("error", next="group_list", msg="user group is not exist!!!")
        try:
            group_obj = Group.objects.get(pk=group_id)
            queryset = group_obj.permissions.all()
        except:
            return redirect("error", next="group_list", msg="user group is not exist!!!")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(GroupPermissionListView, self).get_context_data(**kwargs)
        search_data = self.request.GET.copy()
        group_id = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="user group not exist!!!")
 
        try:
            search_data.pop("page")
        except:
            pass

        context['group_name'] = group_obj
        context['group_id'] = group_id
        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()
        return context

