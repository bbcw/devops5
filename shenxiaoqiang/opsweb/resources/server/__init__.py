from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from resources.models import Server, Serstatus
from django.views.generic import TemplateView, ListView

import datetime

@csrf_exempt
def ServerInfoAutoReport(request):
    if request.method == "POST":
        data = request.POST.dict()
        data['check_update_time'] = datetime.datetime.now()
        try:
            s = Server.objects.get(uuid__exact=data['uuid'])

            # 更新所有字段
            Server.objects.filter(uuid=data['uuid']).update(**data)

            # 更新某一个字段
            #s.hostname = data['hostname']
            #s.check_update_time = datetime.now()
            #s.save(update_fields=['hostname'])

        except Server.DoesNotExist:
            s = Server(**data)
            s.save()
        return HttpResponse("")

class ServerListView(ListView):
    template_name = "server/serverlist.html"
    model = Server
    paginate_by = 10
    before_num = 4
    after_num = 4
    
    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        context["page_range"] = self.get_pagerange(context["page_obj"])

        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&"+search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_num
        end = current_index + self.after_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end+1)

class ModifyServerStatus(TemplateView):
    template_name = "server/modify_server_status.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyServerStatus, self).get_context_data()
        context['serstatus'] = Serstatus.objects.all()
        server_id = self.request.GET.get('sid', '')
        print(server_id)
        try:
            context['server_obj'] = Server.objects.filter(id=server_id)
        except Server.DoesNotExist:
            pass

        return context
