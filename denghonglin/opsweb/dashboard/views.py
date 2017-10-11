from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse
from django.template import Context,loader
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
#from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import unquote_plus
from resources.models import Product,Idc


@login_required
def index(request):
    return render(request,"index.html")

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

# class SuccessView(TemplateView):
#     template_name = "public/success.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(SuccessView, self).get_context_data(**kwargs)
#         success_name = self.kwargs.get("next","")
#         next_url = "/"
#         try:
#             next_url = reverse(success_name)
#         except:
#             pass
#         context['next_url'] = next_url
#         print(next_url)
#         return context


# url页面跳转
class SuccessView(TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        success_name = self.kwargs.get("next","")
        try:
            next_url = reverse(success_name)
        except:
            next_url = unquote_plus(success_name)
        context['next_url'] = next_url
        # print(next_url)
        return context

# class ErrorView(TemplateView):
#     template_name = "public/error.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(ErrorView, self).get_context_data(**kwargs)
#         error_name = self.kwargs.get("next", "")
#         errmsg = self.kwargs.get('msg', "")
#         next_url = "/"
#         try:
#             next_url = reverse(error_name)
#         except:
#             pass
#         context['next_url'] = next_url
#         context['errmsg'] = errmsg
#         return context


# url页面跳转
class ErrorView(TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get('msg', "")
        try:
            next_url = reverse(error_name)
        except:
            next_url = unquote_plus(error_name)
        context['next_url'] = next_url
        context['errmsg'] = errmsg
        return context

class ZnodeView(View):
    def get(self,request):
        ztree = Ztree()
        znode = ztree.get()
        return JsonResponse(znode,safe=False)

class Ztree(object):
    def __init__(self):
        self.data = self.get_product()

    def get_product(self):
        return Product.objects.all()

    def get(self,idc=False):
        ret = []
        for product in self.data.filter(pid=0):
            node = self.process_node(product)
            node["children"] = self.get_children(product.id)
            node["isParent"] = True
            ret.append(node)
        if idc:
            return self.get_idc_node(ret)
        return ret

    def get_children(self,id):
        ret = []
        for product in self.data.filter(pid=id):
            node = self.process_node(product)
            ret.append(node)
        return ret

    def process_node(self,product_obj):
        return {
            "name":product_obj.service_name,
            "id":product_obj.id,
            "pid":product_obj.pid
            }

    def get_idc_node(self,nodes):
        ret = []
        for idc in Idc.objects.all():
            node = {
                "name":idc.idc_name,
                "children":nodes
            }
            ret.append(node)
        return ret




