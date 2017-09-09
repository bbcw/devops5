#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.urlresolvers import reverse

from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from resources.models import Idc
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.mixins import PermissionRequiredMixin


class IdcListView(LoginRequiredMixin, PermissionRequiredMixin,  ListView):
    permission_required = "resources.add_idc"
    # permission_redirect_field_name = "user_list"
    model = Idc
    template_name = "idc/idclist.html"

    def get_queryset(self):
        queryset = super(IdcListView, self).get_queryset()
        idc_name = self.request.GET.get("search_idcname", "")

        if queryset:
            queryset = queryset.filter(name__icontains=idc_name)
        return queryset


    # 第二中 权限验证
    # # @method_decorator(permission_required("resources.add_idc", login_url=reverse("error", kwargs={'next': '/', 'msg': '没有权限'})))
    # @method_decorator(permission_required("resources.add_idc", login_url="/"))
    # #@method_decorator(permission_required("resources.add_idc", login_url="/dashboard/"))
    # def get(self, request, *args, **kwargs):
    #     return super(IdcListView, self).get(self, request, *args, **kwargs)


class IdcCreateView(LoginRequiredMixin, TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):
        ret = {"status": 0}
        name = request.POST.get("name", "")
        idc_name = request.POST.get("idc_name", "")
        address = request.POST.get("address", "")
        username = request.POST.get("username", "")
        user_phone = request.POST.get("user_phone", "")
        email = request.POST.get("email", "")

        try:
            # 也可以直接判断对象是否存在
            # # idc_alreday = Idc.objects.filter(name=name).first()
            idc_alreday = Idc.objects.get(name=name)
            idc_alreday_name = idc_alreday.name
        except:
            idc_alreday_name = ""

        if name and idc_name and address and username and user_phone and email:
            if name == idc_alreday_name:
                ret["errmsg"] = "idc already exist."
                return redirect("error", next="idc_add", msg=ret["errmsg"])
            else:
                data = {
                    "name": name,
                    "idc_name": idc_name,
                    "address": address,
                    "username": username,
                    "user_phone": user_phone,
                    "email": email
                }
                idc_obj = Idc(**data)
                idc_obj.save()
                return redirect("success", next="idc_list")
        else:
            ret["errmsg"] = "列表不能为空"
            return redirect("error", next="idc_add", msg=ret["errmsg"])