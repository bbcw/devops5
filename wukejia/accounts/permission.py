from  django.views.generic import  TemplateView,ListView,View
from django.contrib.auth.models import  Permission,ContentType
from django.core.paginator import Paginator
from django.http import  JsonResponse,HttpResponse
from django.shortcuts import redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.db.models import  Q


class PermissionListView(LoginRequiredMixin,ListView):
    model = Permission
    template_name = 'user/permission_list.html'
    paginate_by = 10
    ordering = 'id'

    def get_queryset(self):
        querset = super(PermissionListView, self).get_queryset()

        #处理搜索条件
        searchword = self.request.GET.get("search_word","")
        if searchword:
            # querset = Permission.content_type.filter(Q(permission__codename__icontains=searchword)| Q(model=searchword))
            querset =  Permission.objects.filter(Q(codename__icontains=searchword)|Q(content_type__model=searchword))
            return  querset
        return  querset



    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)

        try:
            page_num = int(self.request.GET.get("page", 1))
        except:
            page_num = 1


        # all_list = Permission.objects.filter(pk=11).order_by('id')
        all_list = self.get_queryset()
        context['allnums']=len(all_list)

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

        #处理搜索条件
        searchword =  self.request.GET.copy()
        searchword = searchword.dict().get("search_word","")
        print(searchword)
        context['search_word'] = searchword
        context['search_neirong'] = "&search_word=" + searchword


        return context



class PermissionChangeView(LoginRequiredMixin,View):


#change name
    def  post(self,request):
        res = {"status":0}
        pid = request.POST.get("pid","")
        name = request.POST.get("name","")
        print("{0}-{1}".format(pid,name))
        try:
            p = Permission.objects.get(id=pid)
            p.name = name
            p.save()
            res["errmsg"] = "名称描述已修改为：{0}".format(name)
        except Exception as e:
            res["status"]=1
            res["errmsg"]=e.args

        return  JsonResponse(res,safe=False)




class PermissionCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'user/add_permission.html'

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context


    def post(self,request):
        codename = request.POST.get("codename","")
        name = request.POST.get("name","")
        contenttypeID = request.POST.get("content_type","")
        try:
            getcontenttype = ContentType.objects.get(pk=contenttypeID)
        except ContentType.DoesNotExist:
            return  redirect('error',next='permission_list',msg="ContentType 出错球了。")

        if not  codename or codename.find(" ")>=0:
            return  redirect('error',next='permission_list',msg="codename 不合法")

        try:
            Permission.objects.create(codename=codename,name=name,content_type=getcontenttype)
            return  redirect('success',next='permission_list')
        except Exception  as e:
            return  redirect('error',next='permission_list',msg=e.args)



