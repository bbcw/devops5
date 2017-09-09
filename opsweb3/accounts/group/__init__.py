#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import  redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.models import Group
from django.http import JsonResponse, Http404, QueryDict
from django.db import IntegrityError
from django.contrib.auth.models import ContentType, Permission


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "accounts/grouplist.html"


class CreateGroupView(LoginRequiredMixin, View):
    def post(self, request):
        ret = {"status": 0}
        if request.user.has_perm("auth_add_group"):
            group_nmae = request.POST.get('name', "")
            if not group_nmae:
                ret["status"] = 1
                ret["errmsg"] = "组名不能为空"
                return JsonResponse(ret)
            try:
                g = Group(name=group_nmae)
                g.save()
            except IntegrityError:
                ret["status"] = 1
                ret["errmsg"] = "用户组已存在"
            print(ret)
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["errmsg"] = "用户没有操作权限"
            return JsonResponse(ret)


class DeleteGroupView(LoginRequiredMixin, View):
    def delete(self, request):
        ret = {"status": 0}
        if request.user.has_perm("auth.delete_group"):
            data = QueryDict(request.body)
            gid = data.get("gid", "")
            try:
                group_obj = Group.objects.get(pk=gid)
            except Group.DoesNotExist:
                ret["status"] = 1
                ret["errmsg"] = "用户组不存在"
                return JsonResponse(ret)

            if group_obj.user_set.all().count() > 0:
                ret["status"] = 1
                ret["errmsg"] = "用户组有用户"
                return JsonResponse(ret)

            if group_obj.permissions.all().count() > 0:
                ret["status"] = 1
                ret["errmsg"] = "用户组关联着权限"
                return JsonResponse(ret)

            try:
                group_obj.delete()
                return JsonResponse(ret)
            except:
                ret["status"] = 1
                ret["errmsg"] = "没有成功删除用户组"
                return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["errmsg"] = "用户没有操作权限"
            return JsonResponse(ret)


# 就是处理几个gid传值
# class GroupUserListView(View):
#     @method_decorator(login_required)
#     def get(self, request, gid):
#         gid = gid
#         try:
#             group_obj = Group.objects.get(id=gid)
#         except Group.DoesNotExist:
#             group_obj = None
#
#         if group_obj:
#             user_obj = group_obj.user_set.all()
#         return render(request, "accounts/memberlist.html", {"user_obj": user_obj, "current_group": group_obj})


class GroupUserListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/group_userlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupUserListView, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(id=gid)
            # 只是利用models中的一对多关系的反向查询
            context["object_list"] = group_obj.user_set.all()
            context["group_boj"] = group_obj
        except Group.DoesNotExist:
            raise Http404("group does not exist.")
        context['gid'] = gid
        return context


class ModifyGroupPermission(LoginRequiredMixin, TemplateView):
    template_name = "accounts/modify_group_permissions.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermission, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        context["contenttypes"] = ContentType.objects.all()
        if gid:
            context["gid"] = gid
            context["group_permissions"] = self.get_group_permissions(gid)
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户不存在")

    def post(self, request):
        if request.user.has_perm("auth.change_permission"):
            permission_id_list = request.POST.getlist("permission", [])
            gid = request.POST.get("groupid", 0)
            try:
                group_obj = Group.objects.get(id=gid)
            except Group.DoesNotExist:
                return redirect("error", next="group_list", msg="用户不存在")

            if len(permission_id_list) > 0:
                permission_objs = Permission.objects.filter(id__in=permission_id_list)
                group_obj.permissions.set(permission_objs)
            else:
                group_obj.permissions.clear()
            return redirect("success", next="group_list")
        else:
            return redirect("errot", next="group_list", msg="用户没有操作权限")


class GroupPermissionList(LoginRequiredMixin, TemplateView):
    template_name = "accounts/group_permissionlist.html"

    def get_context_data(self, **kwargs):
        context = super(GroupPermissionList, self).get_context_data(**kwargs)
        gid = self.request.GET.get("gid", "")
        try:
            group_obj = Group.objects.get(pk=gid)
            permission_objs = group_obj.permissions.all()
            context["gid"] = gid
            context["object_list"] = permission_objs
            return context
        except Exception:
            return redirect("error", next="group_list", msg="用户组或权限组为空")

    def post(self, request):
        # 这里不实现组列表中权限删除
        print(request.POST, '--------------')
        gid = request.POST.get("groupid", "")
        current_url = request.path
        try:
            netx_url_prefix = "{head}{gid}".format(head="?gid=", gid=gid)
            next_url = "{current_url}{prefix}".format(current_url=current_url, prefix=netx_url_prefix)
        except:
            next_url = ""

        return redirect("success", next=next_url)