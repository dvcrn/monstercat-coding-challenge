from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

class WebappView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch
        :param request: Request
        :type request: HttpRequest
        """

        return super(WebappView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(WebappView, self).get(request, *args, **kwargs)