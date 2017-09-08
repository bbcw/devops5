from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect

class PermissionRequiredMixin(PermissionRequired):    # 定义类名并继承
    permission_redirect_field_name = "dashboard"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            # 定义报错的内容并返回首页
            return redirect("error", next=self.permission_redirect_field_name, msg="没有权限，请联系管理员")
            #return self.handle_no_permission()
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
