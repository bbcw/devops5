from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from resources.models import Product
from django.shortcuts import redirect
from django.contrib.auth.models import User
from resources.forms import ProductForm
import json

class ProductAddView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "resources.add_server"
    template_name = "server/product_add.html"

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context['userlist'] = User.objects.filter(is_superuser=False)
        context['products'] = Product.objects.filter(pid__exact=0)
        return context

    def post(self, request):
        productform = ProductForm(request.POST)

        if productform.is_valid():
            product = Product(**productform.cleaned_data)
            try:
                product.save()
                return redirect("success", next="server_list")
            except Exception as e:
                return redirect("error", next="server_add", msg=e.args)
        else:
            return redirect("error", next="server_add",
                            msg=json.dumps(json.loads(productform.errors.as_json()), ensure_ascii=False))
