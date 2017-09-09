#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q


class PermissionListView(LoginRequiredMixin, ListView):
    model = Permission
    template_name = "accounts/permission_list.html"
    paginate_by = 10
    ordering = "id"

    def get_queryset(self):
        queryset = super(PermissionListView, self).get_queryset()

        # #Poll.objects.get(
        #     Q(pub_date=date(2005, 5, 2)) (|&) Q(pub_date=date(2005, 5, 6)),
        #     question__startswith='Who',
        # )
        permission_search = self.request.GET.get("search_permission", None)
        if permission_search:
            queryset = queryset.filter(Q(codename__icontains=permission_search)|
                                       Q(content_type__model=permission_search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)
        search_data = self.request.GET.copy()

        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context["search_data"] = "{sym}{url}".format(sym="&", url=search_data.urlencode())
        return context


class PermissionAddView(LoginRequiredMixin, ListView):
    model = ContentType
    template_name = "accounts/add_permission.html"

    def post(self, request):
        content_type = request.POST.get("content_type", "")
        codename = request.POST.get("codename", "")
        name = request.POST.get("name", "")

        try:
            content_type = ContentType.objects.get(pk=content_type)
        except ContentType.DoesNotExist:
            return redirect("error", nex="permission_add", msg="模型不存在")

        if not codename and codename.find(" ") >= 0:
            return redirect("error", nex="permission_add", msg="codename 不合法")

        try:
            Permission.objects.create(codename=codename, name=name, content_type=content_type)

        except Exception as e:
            return redirect("error", next="permission_add", msg=e.args)

        return redirect("success", next="permission_list")


