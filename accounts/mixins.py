# coding=utf-8
from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect


class PermissionRequiredMixin(PermissionRequired):
    """覆盖默认的 PermissionRequiredMixin 的 dispatch 方法，自定义相关属性"""

    # 跳转 url 属性，可在继承类里进行覆盖
    permission_redirect_field_name = "dashboard"

    def dispatch(self, request, *args, **kwargs):
        """这里修改的 dispatch 方法覆盖默认的类方法"""
        if not self.has_permission():
            return redirect("error", next="dashboard", msg="没有权限，请联系管理员")
            # return self.handle_no_permission()
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)