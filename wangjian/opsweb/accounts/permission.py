from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from django.http import HttpResponse
from django.shortcuts import redirect

class PermissionListView(ListView):
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 10
    ordering = "id"


class PermissionCreateView(TemplateView):
    template_name = "user/add_permission.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context

    """
    用户通过页面添加权限页面逻辑
    """
    def post(self, request):
        content_type_id = request.POST.get("content_type")
        codename = request.POST.get("codename")
        name = request.POST.get("name")

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect("error", next="permission_list", msg="模型不存在")

        if not codename or codename.find(" ") >=0 :
            return redirect("error", next="permission_list", msg="codename 不合法")

        try:
            Permission.objects.create(codename=codename, content_type=content_type,name=name)
        except Exception as e:
            return redirect("error", next="permission_list", msg=e.args)
        return redirect("success", next="permission_list")


