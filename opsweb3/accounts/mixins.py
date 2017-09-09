#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequred
from django.shortcuts import redirect


class PermissionRequiredMixin(PermissionRequred):
    permission_redirect_field_name = "dashboard"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect("error", next=self.permission_redirect_field_name, msg="没有权限")
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)