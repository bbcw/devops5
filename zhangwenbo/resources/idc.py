from django.views.generic import TemplateView, ListView, View
from django.shortcuts import redirect, render
from resources.models import Idc
from django.db import IntegrityError
from django.http import JsonResponse, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from resources.forms import CreateIdcForm
import json

class CreateIdcView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    创建IDC
    """
    permission_required = "resources.add_idc"
    template_name = "idc/add_idc.html"

    def post(self, request):
        '''
        name = request.POST.get("name", "")
        if name:
            try:
                data = {
                    "name": name,
                    "idc_name": request.POST.get("idc_name", ""),
                    "address": request.POST.get("address", ""),
                    "phone": request.POST.get("phone", ""),
                    "email": request.POST.get("email", ""),
                    "username": request.POST.get("username", "")
                }
                Idc.objects.create(**data)
            except IntegrityError:
                return redirect("error", next="idc_add", msg="idc名称已创建，请重新输入")
            return redirect("success", next="idc_list")
        return redirect("error", next="idc_add", msg="idc名称没输入，请重新输入")
        '''
        idcform = CreateIdcForm(request.POST)
        if idcform.is_valid():
            idc = Idc(**idcform.cleaned_data)
            try:
                idc.save()
                return redirect("success", next="idc_list")
            except Exception as e:
                return redirect("error", next="idc_add", msg=e.args)
        else:
            return redirect("error", next="idc_add", msg=json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False))


class IdcViewList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    '''
    IDC列表
    '''
    permission_required = "resources.view_idc"
    model = Idc
    template_name = "idc/idc_list.html"

class IdcDelete(LoginRequiredMixin, View):
    """
    删除IDC
    """
    def delete(self, request):
        ret = {"status":0}
        if not request.user.has_perm('resources.delete_idc'):
            ret['status'] = 1
            ret['errmsg'] = "没有权限，请联系管理员"
            return JsonResponse(ret)
        data = QueryDict(request.body)
        idc_id = data.get("idcid", "")
        try:
            Idc.objects.filter(id=idc_id).delete()
        except Idc.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "该idc不存在"
            return JsonResponse(ret)
        return  JsonResponse(ret)