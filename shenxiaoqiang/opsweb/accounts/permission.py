from django.contrib.auth.models import Permission, ContentType
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from accounts.forms import CreatePermissionForm
import json
from django.db.models import Q

class PermissionListView(LoginRequiredMixin, ListView):
    template_name = "user/permissionlist.html"
    model = Permission
    paginate_by = 10

    def get_queryset(self):
        queryset = super(PermissionListView, self).get_queryset()  # 存放列表对象(对应表里数据的集合)
        permission_name = self.request.GET.get("search_name","")
        if permission_name:
            #queryset = queryset.filter(codename__exact=permission_name)
            queryset = queryset.filter(Q(codename__exact=permission_name)|Q(content_type__model__icontains=permission_name))
        return queryset


class CreatePermissionView(LoginRequiredMixin, TemplateView):
    template_name = "user/add_permission.html"
    model = ContentType

    def get_context_data(self, **kwargs):
        context = super(CreatePermissionView, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        return context

    def post(self, request):
        # data = {}
        # codename = request.POST.get("codename", "")
        # name = request.POST.get("name", "")
        # content_type_id = request.POST.get("content_type", "")
        # data["codename"] = codename
        # data["name"] = name
        # data["content_type_id"] = content_type_id
        #
        # try:
        #     ContentType.objects.get(pk=content_type_id)
        # except ContentType.DoesNotExist:
        #     return redirect("error",next="permission_add", msg="ContentType is not exist!")
        # if not codename or codename.find(" ") >= 0:
        #     return redirect("error",next="permission_add", msg="codename 不合法")
        #
        # try:
        #     permission = Permission(**data)
        #     permission.save()
        #     return redirect("success", next="permission_list")
        # except Exception as e:
        #     #ret["msg"] = "Idc already exists or other errors"
        #     return redirect("error",next="permission_add", msg=e.args)


    # @method_decorator(permission_required("permission.add_permission", login_url="permission_list"))
    # def get(self, request, *args, **kwargs):
    #    return super(CreatePermissionView, self).get(request, *args, **kwargs)


        # 表单验证
        permissionform = CreatePermissionForm(request.POST)
        if permissionform.is_valid():

            permission = Permission(**permissionform.cleaned_data)

            try:
                permission.save()
                return redirect("success", next="permission_list")
            except Exception as e:
                return redirect("error", next="permission_list", msg=e.args)
        else:
            return redirect("error", next="permission_list",
                            msg=json.dumps(json.loads(permissionform.errors.as_json()), ensure_ascii=False))
