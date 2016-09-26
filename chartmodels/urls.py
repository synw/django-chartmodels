# -*- coding: utf-8 -*-

from django.conf.urls import url
from chartmodels.views import ChartAppView, ChartAllModelsView, ChartsIndexView


urlpatterns = [
    url(r'^models/$', ChartAllModelsView.as_view(), name="allmodels-chart"),
    url(r'^(?P<app>[-._\w]+)/$', ChartAppView.as_view(), name="app-chart"),
    url(r'^', ChartsIndexView.as_view(), name="chart-index")
    ]