from django.contrib.auth.models import Permission, Group, ContentType
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from accounts.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict

class PermissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.add_permission"
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
        content_type_id = request.POST.get("contect_type", "")
        codename = request.POST.get("codename", "")
        name = request.POST.get("name", "")

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect("error", next="permission_list", msg="模型不存在")

        if not codename or codename.find(" ") >=0 :
            return redirect("error", next="permission_list", msg="codename 不合法")

        try:
            Permission.objects.create(codename=codename, content_type=content_type, name=name)
        except Exception as e:
            return redirect("error", next="permission_list", msg=e.args)
        return redirect("sucess", next="permission_list")