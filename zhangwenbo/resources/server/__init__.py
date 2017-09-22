from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from resources.models import Server, Statuses
from resources.forms import StatusesForm
from django.shortcuts import redirect
import datetime, json

@csrf_exempt
def ServerInfoAutoReport(request):
    ##获取服务器端的服务器信息
    if request.method == "POST":
        data = request.POST.dict()
        data['check_update_time'] = datetime.datetime.now()
        try:
            Server.objects.get(uuid__exact=data['uuid'])
            Server.objects.filter(uuid=data['uuid']).update(**data)
        except Server.DoesNotExist:
            s = Server(**data)
            s.save()
        return HttpResponse("")

class ServerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    ##查看server列表
    permission_required = "resources.view_server"
    model = Server
    paginate_by = 10
    before_range_num = 4
    after_range_num = 5
    ordering = "id"
    template_name = "server/server_list.html"

    def get_queryset(self):
        #获取搜索的关键字，过滤出queryset返回
        queryset = super(ServerListView, self).get_queryset()
        hostname = self.request.GET.get("hostname", None)
        inner_ip = self.request.GET.get("inner_ip", None)
        if hostname:
            queryset = queryset.filter(hostname__icontains=hostname)
        if inner_ip:
            queryset = queryset.filter(inner_ip__icontains=inner_ip)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])

        # 复制搜索请求，删除page关键字，保留其它关键字，并返回给前端页码栏
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        if search_data:
            context["search_data"] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end+1)

class ModifyServerStatus(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    ##修改server的状态信息
    permission_required = "resources.change_server"
    template_name = "server/status_modify.html"

    def get_context_data(self, **kwargs):
        ##获取服务器的ID，返回服务器的机器名、ip、id、状态
        context = super(ModifyServerStatus,self).get_context_data(**kwargs)
        sid = self.request.GET.get("server_id", "")
        try:
            server_ll = Server.objects.get(pk=sid)
        except Server.DoesNotExist:
            return redirect("error", next="server_list", msg="服务器不存在")
        context["server_hostname"] = server_ll.hostname
        context["server_ip"] = server_ll.inner_ip
        context["statuses"] = Statuses.objects.all()
        context["server_id"] = server_ll.id
        return context

    def post(self, request):
        ##获取server 的id和status的id，更新server的statuses_id
        status_id = request.POST.get("status", "" )
        server_id = request.POST.get("id", "")
        server = Server.objects.get(pk=server_id)
        server.statuses_id = status_id
        try:
            server.save()
            return redirect("success", next="server_list")
        except Server.DoesNotExist:
            return redirect("error", next="server_list", msg="服务器不存在")

class AddServerStatus(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    ##增加server状态
    permission_required = "resources.add_server"
    template_name = "server/status_add.html"

    def post(self, request):
        ##使用form表单获取status_mark值，新增状态信息
        statusesform = StatusesForm(request.POST)
        if statusesform.is_valid():
            statuses = Statuses(**statusesform.cleaned_data)
            try:
                statuses.save()
                return redirect("success", next="server_list")
            except Exception as e:
                return redirect("error", next="server_list", msg=e.args)
        else:
            return redirect("error", next="server_list",
                            msg=json.dumps(json.loads(statusesform.errors.as_json()), ensure_ascii=False))

