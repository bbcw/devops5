from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.forms import CreatePermissionForm
from django.db.models import Q
import json


class PermissionListView(ListView):
    """权限列表展示页面逻辑"""
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 10                #分页
    ordering = "id"

    # def get_queryset(self):
    #     queryset = super(PermissionListView, self).get_queryset()
    #     content_model = self.request.GET.get('search_model','')
    #     if content_model:
    #         queryset = Permission.objects.filter(content_type__model__contains=content_model)
    #
    #     return queryset


    def get_queryset(self):
        """从数据库中搜索过滤出的数据"""
        queryset = super(PermissionListView, self).get_queryset()
        search = self.request.GET.get('search','')
        if search:
            queryset = Permission.objects.filter(Q(codename__contains=search)|Q(content_type__model__contains=search))
        return queryset


    def get_context_data(self, **kwargs):
        """处理搜索出来的数据传向前端"""
        context = super(PermissionListView, self).get_context_data(**kwargs)
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        if search_data:
            context['search_data'] = "&"+search_data.urlencode()
        return context

class PermissionCreateView(TemplateView):
    """通过页面添加创建权限页面逻辑"""
    template_name = "user/add_permission.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context

    """
    用户通过页面添加权限页面逻辑
    """
    def post(self, request):
        """
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
        """
        permissionform = CreatePermissionForm(request.POST)
        if permissionform.is_valid():
            permission = Permission(**permissionform.cleaned_data)
            try:
                permission.save()
                return redirect("success",next="permission_list")
            except Exception as e:
                return redirect("error",next="permission_list",msg=e.args)
        else:
            return redirect("error",next="permission_list",msg=json.dumps(permissionform.errors.as_json(),ensure_ascii=False))


