from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from resources.models import Server, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.http import urlquote_plus
import datetime

@csrf_exempt
def ServerInfoAutoReport(request):
    if request.method == "POST":
        data = request.POST.dict()
        data['check_update_time'] = datetime.datetime.now()
        try:
            Server.objects.get(uuid__exact=data['uuid'])
            Server.objects.filter(uuid=data['uuid']).update(**data)
            """
            s.hostname = data['hostname']
            s.check_update_time = datetime.now()
            s.save(update_fields=['hostname'])
            """
        except Server.DoesNotExist:
            s = Server(**data)
            s.save()
        return HttpResponse("")

class ServerListView(LoginRequiredMixin,ListView):
    model = Server
    template_name = "server/server_list.html"
    paginate_by = 10
    before_range_num = 5
    after_range_num = 5
    ordering = 'id'

    # def get_queryset(self):
    #     queryset = super(ServerListViews, self).get_queryset()
    #     # # queryset = queryset.exclude(username="admin")
    #     # queryset = queryset.filter(is_superuser=False)
    #
    #     hostname = self.request.GET.get("search_hostname", None)
    #     if hostname:
    #         queryset = queryset.filter(hostname__icontains=hostname)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])
        context['product'] = self.get_product()

        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop('page')
        except:
            pass
        context.update(search_data.dict())
        # context['search_data'] = "&" + search_data.urlencode()
        search_url_str = search_data.urlencode()
        if search_url_str:
            context['search_data'] = "&" + search_url_str
        return context

    def get_product(self):
        ret = {}
        for obj in Product.objects.all():
            ret[obj.id] = obj.service_name
        return ret

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num

        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end+1)

class ServerModifyProductView(TemplateView):
    template_name = "server/server_modify_product.html"

    def get_context_data(self, **kwargs):
        context = super(ServerModifyProductView, self).get_context_data(**kwargs)
        server_id = self.request.GET.get("id", None)
        context['server'] = get_object_or_404(Server, pk=server_id)
        context['products'] = Product.objects.filter(pid=0)
        return context

    def post(self, request):

        next_url = request.GET.get("next", None) if request.GET.get("next", None) else "server_list"
        # '/resources/server/list/?page=4'
        # server_list
        server_id = request.POST.get("id", None)
        service_id = request.POST.get("service_id", None)
        server_purpose = request.POST.get("server_purpose", None)

        try:
            server_obj = Server.objects.get(pk=server_id)
        except Server.DoesNotExist:
            return redirect("error", next="server_list",msg="服务器不存在")

        try:
            product_service_id = Product.objects.get(pk=service_id)
        except Product.DoesNotExist:
            return redirect("error",next="server_list",msg="一级业务线不存在")

        try:
            product_server_purpose = Product.objects.get(pk=server_purpose)
        except Product.DoesNotExist:
            return redirect("error",next="server_list",msg="二级业务线不存在")

        if product_server_purpose.pid != product_service_id.id:
            raise Http404
        server_obj.service_id = product_service_id.id
        server_obj.server_purpose = product_server_purpose.id
        server_obj.save(update_fields=["service_id","server_purpose"])

        return redirect(reverse("success",kwargs={"next":urlquote_plus(next_url)}))


class GetServerListView(View):
    def get(self,request):
        server_purpose = request.GET.get("server_purpose", None)
        # 获取某台机器的所有信息

        # 获取某个业务线下的所有机器列表

        if server_purpose:
            queryset = Server.objects.filter(server_purpose=server_purpose).values("id","hostname","inner_ip")
            return JsonResponse(list(queryset), safe=False)
        # ....
        return JsonResponse([], safe=False)

