from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

class myPermissionRequiredMixin(PermissionRequiredMixin):
    next_path = ''
    permission_required = 'auth.view_user'
    msg="没有权限,请联系管理员啊啊啊啊啊！"
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('error',next=self.next_path,msg=self.msg)
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)

