# -*- coding: utf-8 -*-

from __future__ import print_function
from django.http.response import Http404
from django.views.generic import TemplateView
from chartmodels.utils import get_all_apps_models


class UsersDashView(TemplateView):
    template_name = "chartmodels/dashboards/users.html"


class AllModelsDashView(TemplateView):
    template_name = "chartmodels/all_models.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        context = super(AllModelsDashView, self).get_context_data(**kwargs)
        return context


class ModelDashView(TemplateView):
    template_name = "chartmodels/app.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        context = super(ModelDashView, self).get_context_data(**kwargs)
        appname = kwargs["app"]
        context["app"] = appname
        context["chart"] = "chartflo/charts/app_" + appname + ".html"
        return context


class ChartsIndexView(TemplateView):
    template_name = "chartmodels/index.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        context = super(ChartsIndexView, self).get_context_data(**kwargs)
        appmodels = get_all_apps_models(names_only=True)
        context['appmodels'] = appmodels
        return context
