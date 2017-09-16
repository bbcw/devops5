#!/usr/bin/python
# coding=utf8
from django.contrib.auth.models import Group, User, ContentType, Permission
from django.views.generic import View, TemplateView, ListView
from django.http import HttpResponse, JsonResponse, QueryDict, Http404
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import CreateGroupForm
import json


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "group/grouplist.html"


class GroupCreateView(LoginRequiredMixin ,View):
    """用户组创建视图"""
    def post(self, request):
        ret = {'status': 0}
        # # print(request.POST)     # 一个 QueryDict
        # group_name = request.POST.get("name", "")           # 获取 ajax 请求过来的变量
        #
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
        #
        # return JsonResponse(ret)
        groupform = CreateGroupForm(request.POST)
        # print(groupform)

        if groupform.is_valid():
            # print(groupform.cleaned_data)
            g = Group(name=groupform.cleaned_data.get("name"))
            g.save()
        else:
            # return redirect("error", next="group_list",
            #                 msg=json.dumps(json.loads(groupform.errors.as_json()), ensure_ascii=False))
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"
        return JsonResponse(ret)

class GroupUserList(LoginRequiredMixin, TemplateView):
    """用户组操作的逻辑"""
    template_name = 'group/group_userlist.html'

    def get_context_data(self, **kwargs):
        """用户组内的成员列表展示"""
        context = super(GroupUserList, self).get_context_data(**kwargs)

        gid = self.request.GET.get("gid", "")          # 获取前端传递的 gid
        try:
            group_obj = Group.objects.get(id=gid)       # 根据 gid 查询 group name
            '''
            get 会抛出两个异常
                - 取不到
                - 取到超过1条
            '''
            context['object_list'] = group_obj.user_set.all()   # 取出用户组内全部的用户对象
        except Group.DoesNotExist:
            raise Http404("用户组不存在")

        context['gid'] = gid
        return context


class GroupDeleteView(LoginRequiredMixin, View):
    """删除 Group 的逻辑，响应前端 ajax 请求"""
    def post(self, request):
        ret = {'status': 0}
        group_id = request.POST.get('group_id', '')     # 获取前端 ajax 传递过来的 gid

        # 获取 idc_id 后进行对应的删除，异常给予报错提示
        try:
            group = Group.objects.get(pk=group_id)
            # 判断组内有无成员，无成员才删除
            # print(group.user_set.count(), group.permissions.count())
            if group.user_set.count() == 0 and group.permissions.count() == 0:
                group.delete()
            else:
                ret['status'] = 1
                ret['errmsg'] = "该组下有成员或有对应的权限，无法删除"
        except Group.DoesNotExist:
            ret['stauts'] = 1
            ret['errmsg'] = "Group不存在"
        return JsonResponse(ret)


class ModifyGroupPermissionList(LoginRequiredMixin, TemplateView):
    """修改用户组权限逻辑"""
    template_name = "group/modify_group_permission.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionList, self).get_context_data()
        context['contenttypes'] = ContentType.objects.all()
        context['group'] = self.request.GET.get("gid")
        context['group_permissions'] = self.get_group_permissions(context["group"])
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

    def post(self, request):
        # print(request.POST)
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


class GroupPermissionListView(LoginRequiredMixin, View):
    """用户组查看权限逻辑, 响应前端 ajax 请求"""
    def get(self, request):
        # print(request.body)
        ret = {'status': 0}
        gid = request.GET.get('group_id', '')   # 获取前端传递的变量

        try:
            group = Group.objects.get(pk=gid)       # 取组对象
            group_permissions = group.permissions.all()     # 组权限的 queryset
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        except Permission.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "权限不存在"

        return JsonResponse(list(group_permissions.values("name", "codename")), safe=False)
