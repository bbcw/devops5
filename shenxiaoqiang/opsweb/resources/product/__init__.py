from django.http import HttpResponse
from resources.models import Product
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from resources.forms import CreateProductForm
from django.shortcuts import redirect
import json

class CreateProductView(TemplateView):
    template_name = "server/add_product.html"

    def get_context_data(self):
        context = super(CreateProductView, self).get_context_data()
        context["userlist"] = User.objects.filter(is_superuser=False)
        context["products"] = Product.objects.filter(pid=0)
        return context

    def post(self, request):

        productform = CreateProductForm(request.POST)
        if productform.is_valid():
           product = Product(**productform.cleaned_data)
           try:
               product.save()
               return redirect("success", next="product_add")
           except Exception as e:
               return redirect("error",next="product_add", msg=e.args)
        else:
           return redirect("error",next="product_add", msg=json.dumps(json.loads(productform.errors.as_json()), ensure_ascii=False))

        #print(request.POST)
        #return HttpResponse("")

        #<QueryDict: {'csrfmiddlewaretoken': ['fuu3hC3BJtDkfbjr7kKLJbRpjOfJ0qXh5VjtVw9aq1n4fECpRQAl8ElPrMEZs8Pe'], 'service_name': ['soma'], 'module_letter': ['soma'], 'pid': ['0'], 'dev_interface': ['rock_0@126.com'], 'op_interface': ['rock_0@126.com']}>
