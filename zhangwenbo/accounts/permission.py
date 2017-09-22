from django.contrib.auth.models import Permission, Group, ContentType
from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from accounts.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from accounts.forms import CreatePermissionForm
import json

class PermissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.view_permission"
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 8

    def get_queryset(self):
        #根据搜索条件过滤出queryset
        queryset = super(PermissionListView, self).get_queryset()
        permission_word = self.request.GET.get("search_username", None)
        ct = ContentType.objects.all()
        try:
            if permission_word:
                ct_fil = ct.filter(model__contains=permission_word)
                ct_ad = [ i.id for i in ct_fil ]
                queryset = queryset.filter(content_type_id__in=ct_ad).filter(codename__icontains=permission_word)
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)
        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        if search_data:
            context["search_data"] = "&"+search_data.urlencode()
        return context

class PermissionAdd(LoginRequiredMixin, PermissionRequiredMixin,TemplateView):
    permission_required = "auth.add_permission"
    template_name = "user/permission_add.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionAdd, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        return context

    def post(self, request):
        ##使用Form类处理前端输入的内容
        permissionform = CreatePermissionForm(request.POST)
        if permissionform.is_valid():
            permission = Permission(**permissionform.cleaned_data)
            try:
                permission.save()
                return redirect("success", next="permission_list")
            except Exception as e:
                return redirect("error", next="permission_list", msg=e.args)
        else:
            return redirect("error", next="permission_list", msg=json.dumps(json.loads(permissionform.errors.as_json()), ensure_ascii=False))

class ModifyPermissionName(LoginRequiredMixin, View):
    ##修改权限名称
    def post(self, request):
        ret = {"status": 0}
        if not request.user.has_perm('auth.change_permission'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        get_per_id = request.POST.get("permission_id", "")
        get_per_name = request.POST.get("permission_name", "")
        try:
            permission = Permission.objects.get(pk=get_per_id)
        except Permission.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "权限不存在"
            return JsonResponse(ret)
        try:
            permission.name = get_per_name
            permission.save()
        except Exception as e:
            ret['status'] = 1
            ret['errmsg'] = e.args
        return JsonResponse(ret)



