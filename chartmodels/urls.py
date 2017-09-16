# -*- coding: utf-8 -*-

from django.conf.urls import url
from chartmodels.views import ChartsIndexView, AllModelsDashView, ModelDashView, UsersDashView


urlpatterns = [
    url(r'^all/$', AllModelsDashView.as_view(), name="allmodels-chart"),
    url(r'^users/$', UsersDashView.as_view()),
    url(r'^(?P<app>[-._\w]+)/$', ModelDashView.as_view(), name="app-chart"),
    url(r'^', ChartsIndexView.as_view(), name="chart-index")
]
