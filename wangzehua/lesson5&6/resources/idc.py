from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from resources.models import Idc
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from .forms import CreateIdcForm

class CreateIdcView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "idc/add_idc.html"
    permission_required = "resources.add_idc"
    permission_redirect_field_name = "index"

    def post(self, request):
        '''
        print(request.POST)
        print(reverse("success", kwargs={"next": "user_list"}))

        #先取到post数据
        name = request.POST.get("name", "")
        idc_name = request.POST.get("idc_name", "")
        address = request.POST.get("address", "")
        username = request.POST.get("username", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        #对数据进行验证
        errmsg = []
        if not name:
            errmsg.append("idc简称不能为空")
        if not idc_name:
            errmsg.append("idc名称不能为空")

        if errmsg:
            return redirect("error", next="idc_add", msg=json.dumps(errmsg))

        #将数据插入到数据库，创建模型对象
        data = Idc()
        data.name = name
        data.idc_name = idc_name
        data.address = address
        data.username = username
        data.phone = phone
        data.email = email

        try:
            data.save()
            return redirect("success", next="idc_list")
        except Exception as e:
            errmsg = "人为失败"
            return redirect("error", next="idc_add", msg=errmsg)


        try:
            data.save()
            return redirect("success", next="idc_list")
        except:
            errmsg = "人为失败"
            return redirect("error", next="idc_add", msg=errmsg)
        #return HttpResponse("")

        '''
        idcform = CreateIdcForm(request.POST)
        if idcform.is_valid():
            print("验证成功")
            print(idcform.cleaned_data)
            idc = Idc(**idcform.cleaned_data)
            try:
                idc.save()
                return redirect("success", next="idc_list")
            except Exception as e:
                return redirect("error", next="idc_add", msg=e.args)
        else:
            return redirect("error", next="idc_add", msg=json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False))


class IdcListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "idc/idc_list.html"
    model = Idc
    permission_required = "resources.view_idc"
    permission_redirect_field_name = "user_list"

    '''
    @method_decorator(permission_required("auth.add_user", login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(IdcListView, self).get(request, *args, **kwargs)
    '''