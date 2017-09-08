from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect

class PermissionRequiredMixin(PermissionRequired):

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect("error", next=self.permission_redirect_field_name, msg="没有权限")
            #return self.handle_no_permission()
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
