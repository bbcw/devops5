# coding=utf-8

from django.views.generic import View, TemplateView, ListView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group, Permission, ContentType
from accounts.forms import CreatePermissionForm
import json
from django.contrib.auth.mixins import LoginRequiredMixin



class PermissionListView(LoginRequiredMixin, ListView):
    """权限展示列表逻辑"""
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 10


class PermissionAddView(LoginRequiredMixin, TemplateView):
    """增加权限逻辑"""
    template_name = "user/add_permission.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionAddView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()     # 向前端传递 content_type
        return context

    def post(self, request):
        permissionform = CreatePermissionForm(request.POST)     # 获取表单数据

        # 验证表单数据合法性
        if permissionform.is_valid():
            permissionform = Permission(**permissionform.cleaned_data)
            try:
                permissionform.save()
                return redirect("success", next="permission_list")
            except Exception as e:
                return redirect("error", next="permission_list", msg=e.args)

        else:
            return redirect("error", next="permission_list",
                            msg=json.dumps(json.loads(permissionform.errors.as_json()), ensure_ascii=False))


