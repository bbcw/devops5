from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from resources.models import Idc
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from .forms import CreateIdcForm

class CreateIdcView(LoginRequiredMixin, TemplateView):
    template_name = "idc/add_idc.html"

    def post(self, request):

        # 在view中权限验证
        if not request.user.has_perm('auth.add_idc'):
            return HttpResponse('Forbidden')

        print(request.POST)

        '''
         # < QueryDict: {'csrfmiddlewaretoken': ['wfP0NagrLCAbYBwIqje87xk7iEcIkYLDkpJeSvgLJ0MIpbQW5uq9XMSlyoNamrjP'],
         #              'name': ['12'], 'idc_name': ['12'], 'address': ['1'], 'username': ['1'], 'user_phone': ['1'],
         #              'mail': ['1']} >

        # 1 先取到前端给后端post的数据
        name = request.POST.get("name", "")
        idc_name = request.POST.get("idc_name", "")
        address = request.POST.get("address", "")
        username = request.POST.get("username", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
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
            return redirect("error", next="idc_add", errmsg=e.args)
        return redirect("success", next="idc_list")
        '''
        idcform = CreateIdcForm(request.POST)
        if idcform.is_valid():
            idc = Idc(**idcform.cleaned_data)
            try:
                idc.save()
                return redirect('success', next='idc_list')
            except Exception as e:
                return redirect('error', next='idc_list', errmsg=e.args)
        else:
            print(idcform.errors.as_data())
            return redirect('error', next='idc_list',
                            errmsg=json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False))

class IdcListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'resources.add_idc'
    permission_redirect_field_name = 'user_list'
    model = Idc
    template_name = 'idc/list_idc.html'



