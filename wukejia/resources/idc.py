from django.views.generic import  TemplateView,ListView
from django.shortcuts import redirect,reverse
from  django.http import  HttpResponse
from resources.models import Idc
import  json
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import myPermissionRequiredMixin

class CreateIdcView(LoginRequiredMixin,myPermissionRequiredMixin,TemplateView):
    permission_required = ('resources.view_idc','resources.add_idc')
    msg = "你没有添加idc的权限，请联系管理员。"
    next_path = 'idc_list'
    template_name = 'idc/add_idc.html'

    def post(self,request):
        # print(reverse("success",kwargs={'next':'user_list'}))
        # return redirect('success',next='user_list')
        querydict = request.POST
        name = querydict.get("name","")
        idc_name = querydict.get("idc_name","")
        address = querydict.get("address","")
        phone = querydict.get("phone","")
        email = querydict.get("email","")
        username = querydict.get("username","")

        data = querydict.dict()
        data.pop("csrfmiddlewaretoken")
        print(data)
        idc = Idc(**data)

        errmsg = []
        if not name:
            errmsg.append("IDC简称不能为空")
        if not idc_name:
            errmsg.append("IDC名称不能为空")

        if errmsg:
            return redirect('error', next='idc_add', msg=json.dumps(errmsg,ensure_ascii=False), )

        try:
            idc.save()
            return  redirect('success','idc_list')
        except Exception as e:
            return  redirect('error',next='idc_add',msg=e.args)

        return HttpResponse("nihao")

class IdcListView(LoginRequiredMixin,myPermissionRequiredMixin,ListView):
    permission_required = ('resources.view_idc',)
    msg = "你没有查看idc列表的权限，请联系管理员。"

    model = Idc
    template_name = "idc/idc_list.html"
    paginate_by = 8
    ordering = 'id'

    def get_context_data(self, **kwargs):
        context = super(IdcListView, self).get_context_data(**kwargs)
        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1
        all_list = Idc.objects.all()
        paginator = Paginator(all_list, self.paginate_by)
        zong = paginator.num_pages
        if page_num > zong:
            page_num = zong
        if page_num < 0:
            page_num = 1

        context['page_obj'] = paginator.page(page_num)
        context['object_list'] = context['page_obj'].object_list

        current_page = context['page_obj'].number - 1
        startpage = current_page - 4
        endpage = current_page + 5

        sdiffpage = 0
        ediffpage = 0

        if startpage < 0:
            sdiffpage = -startpage

        if endpage > zong:
            ediffpage = endpage - zong

        endpage += sdiffpage
        startpage -= ediffpage

        if endpage > zong:
            endpage = zong
        if startpage < 0:
            startpage = 0

        # print(startpage, endpage)
        context['page_range'] = context['paginator'].page_range[startpage:endpage]

        return context







