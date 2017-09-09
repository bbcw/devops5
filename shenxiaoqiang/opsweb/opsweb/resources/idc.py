# coding:utf8
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, JsonResponse
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from resources.models import Idc

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

#调用自定义的验证视图
from accounts.mixins import PermissionRequiredMixin

class IdcListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "idc/idclist.html"
    model = Idc
    ordering = "id"
    # 加载PermissionRequiredMixin类执行权限验证
    permission_required = "resource.view_idc"

    # 加载自定义的PermissionRequiredMixin 类执行权限验证跳转
    permission_redirect_field_name = "user_list"

    def get_queryset(self):
        queryset = super(IdcListView, self).get_queryset()  # 存放列表对象(对应表里数据的集合)
        idcname = self.request.GET.get("search_idcname","")
        if idcname:
            queryset = queryset.filter(name__icontains=idcname)
        return queryset
   
    # 使用装饰器 验证
    #@method_decorator(permission_required("resources.add_idc", login_url="/"))
    #def get(self, request, *args, **kwargs):
    #    return super(IdcListView, self).get(request, *args, **kwargs)

class CreateIdcView(LoginRequiredMixin, TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):

        #print(request.POST)
        #print(reverse("success",kwargs={"next":"user_list"}))
        #return redirect("success", next="user_list")
        #return redirect("error",next="idc_add", msg="Please resubmit!!!")

        ret = {}
        data = {}

        for k in request.POST:
            data[k] = request.POST.get(k,"")
        data.pop("csrfmiddlewaretoken")
        #print(data)
        #if not data["name"]:
        #    ret["msg"] = "name is null!"
        #    return redirect("error", next="idc_add", msg=ret["msg"])
        try:
            idc = Idc(**data)
            idc.save()
            return redirect("success", next="idc_list")
        except Exception as e:
            #ret["msg"] = "Idc already exists or other errors"
            return redirect("error",next="idc_add", msg=e.args)


    @method_decorator(permission_required("resources.add_idc", login_url="idc_list"))
    def get(self, request, *args, **kwargs):
       return super(IdcListView, self).get(request, *args, **kwargs)
