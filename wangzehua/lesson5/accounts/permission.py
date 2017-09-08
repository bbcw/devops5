from django.views.generic import  ListView, TemplateView
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from resources.models import Idc
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin


class PermissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "user/permission_list.html"
    model = Permission
    paginate_by = 10
    ordering = "id"
    permission_required = "auth.add_permission"
    permission_redirect_field_name = "index"

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)

        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context["search_data"] = "&" + search_data.urlencode()

        return context

    def get_queryset(self):
        queryset = super(PermissionListView, self).get_queryset()  #存放所有对象的集合，列表被重定义，每个元素是个对象
        #[<object>]
        data = self.request.GET.get("search_model_codename", None)
        if data:
            tmp = queryset
            args = (Q(name__icontains = data) | Q(codename__icontains = data))
            queryset = queryset.filter(Q(content_type__model__icontains = data) | Q(codename__icontains = data))
        return queryset

class PermissionAdd(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "user/add_permission.html"
    permission_required = "auth.add_permission"
    permission_redirect_field_name = "index"

    def get_context_data(self, **kwargs):
        context = super(PermissionAdd, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context

    def post(self, request):
        print(request.POST)
        content_type_id = request.POST.get("content_type")
        codename = request.POST.get("codename")
        name = request.POST.get("name")

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect("error", next="permission_list", msg="模型不存在")

        if not codename or codename.find(" ") >= 0:
            return redirect("error", next="permission_list", msg="codename不合法")

        try:
            Permission.objects.create(codename = codename, name = name, content_type = content_type)
        except Exception as e:
            return redirect("error", next="permission_list", msg=e.args)

        return redirect("success", next="permission_list")
