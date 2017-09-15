from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from resources.models import Idc
from django.http import HttpResponse
from django.shortcuts import redirect
import json
from accounts.forms import CreatePermissionForm
from django.contrib.auth.mixins import LoginRequiredMixin

class PermissionListView(LoginRequiredMixin, ListView):
    model = Permission
    template_name = 'user/permission_list.html'
    paginate_by = 10
    ordering = 'id'

    # 权限列表搜索，codename与model
    def get_queryset(self):
        queryset = super().get_queryset()

        print(queryset)
        model = self.request.GET.get("search_model", None)
        #codename = self.request.GET.get("search_codename", None)
        if model:
            queryset = queryset.filter(content_type__model__exact=model)

        return queryset

class PermissionCreateView(TemplateView):
    template_name = 'user/add_permission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()

        return context

    def post(self, request):

        # 在view中权限验证
        if not request.user.has_perm('auth.add_permission'):
            return HttpResponse('Forbidden')

        print(request.POST)
        '''
        content_type_id = request.POST.get("content_type")
        codename = request.POST.get("codename")
        name = request.POST.get("name")

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect('error', next='permission_list', errmsg='模型不存在')

        if not codename or codename.find(' ') >= 0 :
            return redirect('error', next='permission_list', errmsg='codename不合法')

        try:
            Permission.objects.create(codename=codename, content_type=content_type, name=name)
        except Exception as e:
            return redirect('error', next='permission_list', msg=e.args)

        return redirect('success', next='permission_list')
        '''
        permissionform = CreatePermissionForm(request.POST)
        if permissionform.is_valid():
            permission = Permission(**permissionform.cleaned_data)
            try:
                permission.save()
                return redirect("success", next="permission_list")
            except Exception as e:
                return redirect("error", next="permission_list", errmsg=e.args)
        else:
            return redirect("error", next="idc_list",
                            errmsg=json.dumps(json.loads(permissionform.errors.as_json()), ensure_ascii=False))