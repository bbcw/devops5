from django.shortcuts import reverse
# Create your views here.
from django.http import HttpResponse
from django.views.generic import  TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


'''
@login_required
def index(request):
    return render(request,"index.html")
'''


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'

    # @method_decorator(login_required)
    # def get(self, request, *args, **kwargs):
    #     return  super(IndexView, self).get(request,*args,**kwargs)




class SuccessView(LoginRequiredMixin,TemplateView):
    template_name = 'public/success.html'
    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        success_name = self.kwargs.get("next")
        # print(reverse(success_name))
        try:
            context['next_url'] = reverse(success_name)
        except:
            context['next_url'] = "/"
        return  context


class ErrorView(LoginRequiredMixin,TemplateView):
    template_name = "public/error.html"
    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        error_name = self.kwargs.get("next","")
        errmsg = self.kwargs.get("msg","")

        # print(reverse(success_name))
        context["errmsg"] = errmsg
        try:
            context['next_url'] = reverse(error_name)
        except:
            context['next_url'] = "/"

        return  context
