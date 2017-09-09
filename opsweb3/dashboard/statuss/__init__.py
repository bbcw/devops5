#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "public/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)

        success_name = self.kwargs.get("next", "")

        next_url = "/"
        try:
            # next_url = reverse(success_name)
            next_url = self.deal_nexturl_method(success_name)
        except:
            pass

        context["next_url"] = next_url
        return context

    def deal_nexturl_method(self, nexturl):
        if nexturl:
            if nexturl.startswith("/") and "?" in nexturl:
                next_url = nexturl
            else:
                next_url = reverse(nexturl)
        return next_url


class ErrorView(LoginRequiredMixin, TemplateView):
    template_name = "public/error.html"

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)

        error_name = self.kwargs.get("next", "")
        errmsg = self.kwargs.get("msg", "")
        next_url = "/"
        try:
            next_url = reverse(error_name)
        except:
            pass
        context["next_url"] = next_url
        context["errmsg"] = errmsg
        return context