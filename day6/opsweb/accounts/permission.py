from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.forms import CreatePermissionForms
from django.contrib.auth.mixins import LoginRequiredMixin
import json

class PermissionListView(LoginRequiredMixin,ListView):
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 10
    odering = "id"

    '''权限的model搜索'''
    def get_queryset(self):
        # print (self.request.get_full_path())
        queryset = super(PermissionListView, self).get_queryset()
        pmodel = self.request.GET.get("search_model","")
        if pmodel:
            queryset = Permission.objects.filter(content_type__model__contains=pmodel)
        return queryset

class PermissionCreateView(LoginRequiredMixin,TemplateView):
    template_name = "user/add_permission.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context

    def post(self,request):
        """
        context_type_id = request.POST.get("content_type")
        codename = request.POST.get("codename")
        name = request.POST.get("name")

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect("error",next="permission_list",msg="模型不存在")

        if not codename or codename.find(" ") >= 0:
            return redirect("error",next="permission_list",msg="codename不合法")

        try:
            Permission.objects.create(codename=codename, content_type=content_type,name=name)
        except Exception as e:
            return redirect("error",next="permission_list",msg=e.args)
        return redirect("success",next="permission_list")
        """

        # form表单验证
        permissionform = CreatePermissionForms(request.POST)
        if permissionform.is_valid():
            permission = Permission(**permissionform.cleaned_data)
            try:
                permission.save()
                return redirect("success",next="permission_list")
            except Exception as e:
                return redirect("error",next="permission_list",msg=e.args)
        else:
            return redirect("error",next="permission_list",
                                            msg=json.dumps(json.loads(permissionform.errors.as_json()),ensure_ascii=False))
