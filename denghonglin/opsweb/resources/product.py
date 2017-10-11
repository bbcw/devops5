from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from resources.models import Product, Idc
from django.shortcuts import redirect
from resources.forms import ProductForm
from django.http import JsonResponse

import json

class ProductAddView(TemplateView):
    template_name = "product/add_product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context['userlist'] = User.objects.filter(is_superuser=False)
        context['products'] = Product.objects.filter(pid__exact=0)
        return context

    def post(self, request):
        # print(request.POST)
        productform = ProductForm(request.POST)

        if productform.is_valid():
            product = Product(**productform.cleaned_data)
            try:
                product.save()
                return redirect("success", next="idc_list")
            except Exception as e:
                return redirect("error", next="idc_list",msg=e.args)
        else:
            return redirect("error", next="idc_list",
                            msg=json.dumps(json.loads(productform.errors.as_json()), ensure_ascii=False))

class ProductGetView(View):
    def get(self, request):
        ret = {"status":0}

        # 1 根据product id，取指定的一条记录
        p_id = self.request.GET.get("id",None)
        p_pid = self.request.GET.get("pid",None)
        if p_id:
            ret["data"] = self.get_obj_dict(p_id)
        # 2 根据product pid，取出多条记录
        if p_pid:
            ret["data"] = self.get_products(p_pid)
        # 3 不传任何值，取出所有记录
        return JsonResponse(ret)

    def get_obj_dict(self, p_id):
        try:
            obj = Product.objects.get(pk=p_id)
            ret = obj.__dict__
            ret.pop("_state")
            return ret
        except Product.DoesNotExist:
            return {}

    def get_products(self,pid):
        return list(Product.objects.filter(pid=pid).values())

class ProductManageView(TemplateView):
    template_name = "product/product_manage.html"

    def get_context_data(self, **kwargs):
        context = super(ProductManageView,self).get_context_data(**kwargs)
        context['ztree'] = Ztree().get()
        return context

class Ztree(object):
    def __init__(self):
        self.data = self.get_product()

    def get_product(self):
        return Product.objects.all()

    def get(self, idc=False):
        ret = []
        for product in self.data.filter(pid=0):
            node = self.process_node(product)
            node["children"] = self.get_children(product.id)
            node["isParent"] = "true"
            ret.append(node)
        if idc:
            return self.get_idc_node(ret)
        return ret

    def get_children(self, id):
        ret = []
        for product in self.data.filter(pid=id):
            node = self.process_node(product)
            ret.append(node)
        return ret

    def process_node(self, product_obj):
        return {
            "name": product_obj.service_name,
            "id": product_obj.id,
            "pid": product_obj.pid
        }

    def get_idc_node(self, nodes):
        ret = []
        for idc in Idc.objects.all():
            node = {
                "name": idc.idc_name,
                "children": nodes
            }
            ret.append(node)
        return ret
