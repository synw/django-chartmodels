from __future__ import print_function
from django.http.response import Http404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.utils.html import strip_tags
from chartflo.factory import ChartDataPack
from chartmodels.utils import get_all_apps_models, get_all_models
from introspection.inspector import inspect


class ChartsIndexView(TemplateView):
    template_name = "chartmodels/index.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        context = super(ChartsIndexView, self).get_context_data(**kwargs)
        appmodels = get_all_apps_models(names_only=True)
        context['appmodels'] = appmodels
        return context


class ChartAllModelsView(TemplateView):
    template_name = "chartmodels/chart_models.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        context = super(ChartAllModelsView, self).get_context_data(**kwargs)
        charttype = "pie"
        if "c" in self.request.GET:
            charttype = strip_tags(self.request.GET['c'])
        dataset = {}
        num_apps = len(settings.INSTALLED_APPS)
        num_models = 0
        num_instances = 0
        P = ChartDataPack()
        for appname in inspect.appnames:
            models, err = inspect.models(appname)
            if err is not None:
                print(err)
            for model in models:
                try:
                    num = model.objects.all().count()
                except Exception as e:
                    print(e)
                    continue
                num_models += 1
                num_instances += num
                dataset[model.__name__] = num
        datapack = P.package("chart", "All models", dataset, True)
        datapack['legend'] = True
        datapack['export'] = False
        context['title'] = _(u"all models")
        context['num_models'] = num_models
        context['num_apps'] = num_apps
        context['num_instances'] = num_instances
        context['datapack'] = datapack
        context['template_path'] = "chartflo/charts/" + charttype + ".html"
        return context


class ChartAppView(TemplateView):
    template_name = 'chartmodels/chart.html'

    def get_context_data(self, **kwargs):
        context = super(ChartAppView, self).get_context_data(**kwargs)
        charttype = "pie"
        if "c" in self.request.GET:
            charttype = strip_tags(self.request.GET['c'])
        dataset = {}
        P = ChartDataPack()
        appname = kwargs['app']
        models = get_all_models(appname)
        for model in models:
            try:
                num = model.objects.all().count()
                dataset[model.__name__] = num
            except ImportError as e:
                print(str(e) + " Model not found")
        datapack = P.package("chart", "Data", dataset)
        context['title'] = appname
        context['datapack'] = datapack
        context['template_path'] = "chartflo/charts/" + charttype + ".html"
        return context
