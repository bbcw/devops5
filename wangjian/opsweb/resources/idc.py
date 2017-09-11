from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse,JsonResponse,QueryDict
from resources.models import Idc
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from .forms import CreateIdcForm


class CreateIdcView(TemplateView):
    """创建IDC页面逻辑 响应前端ajax"""
    template_name = "idc/add_idc.html"
    def post(self, request):

        #< QueryDict: {'csrfmiddlewaretoken': ['tBM48BGH7RZNbgEgZlAToE63SfYJVIutOqjgebQMrhE6IEMnaVtNZLeSsiLWfjTq'],
        #              'name': ['yz'], 'idc_name': ['北京亦庄机房'], 'address': ['北京亦庄机房'], 'username': ['rock'],
        #              'user_phone': ['12345678'], 'mail': ['rock@51reboot.com']} >
        # 1 先取到前端给后端post的数据

        """
        name = request.POST.get("name", "")
        idc_name = request.POST.get("idc_name", "")
        address = request.POST.get("address", "")
        username = request.POST.get("username", "")
        phone = request.POST.get("user_phone", "")
        email = request.POST.get("mail", "")
        # 2 对数据进行验证
        errmsg = []
        if not name:
            errmsg.append("idc简称不能为空")
        if not idc_name:
            errmsg.append("idc名称不能为空")

        if errmsg:
            return redirect("error", next="idc_add", msg=json.dumps(errmsg))

        # 3 将数据插入到数据库：创建模型对象
        idc = Idc()
        idc.name = name
        idc.idc_name = idc_name
        idc.address = address
        idc.username = username
        idc.phone = phone
        idc.email = email

        try:
            idc.save()
        except Exception as e :
            return redirect("error", next="idc_add", msg=e.args)
        return redirect("success", next="idc_list")
        """

        idcform = CreateIdcForm(request.POST) #使用forms表单中CreateIdcForm进行验证
        if idcform.is_valid():                #如果表单数据是有效的
            idc = Idc(**idcform.cleaned_data)
            try:
                idc.save()
                return redirect("success", next="idc_list")
            except Exception as e:
                return redirect("error", next="idc_list", msg=e.args)
        else:
            return redirect("error",next="idc_list",msg=json.dumps(json.loads(idcform.errors.as_json()),ensure_ascii=False))

class IdcListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = "resources.view_idc"
    permission_redirect_field_name = "user_list"
    model = Idc
    template_name = "idc/idc_list.html"

    """
    在idc_list.html页面中有删除idc的button 这里处理的是删除idc的逻辑 delete方法是要从QueryDict里取出data数据 然后实例化idc的object 进行删除
    """
    def delete(self,request):
        ret = {"status":0}
        #print(QueryDict(request.body))
        data = QueryDict(request.body)
        idc_obj = Idc.objects.get(id=data.get('id',''))
        idc_obj.delete()
        return  JsonResponse(ret)