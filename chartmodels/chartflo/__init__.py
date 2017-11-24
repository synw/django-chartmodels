# -*- coding: utf-8 -*-

from __future__ import print_function
from introspection.inspector import inspect
from goerr import err
from goerr.colors import colors
from chartflo.charts import chart
from chartflo.models import Chart
from chartmodels.conf import EXCLUDE


OK = "[" + colors.bold("ok") + "] "


def get_data():
    dataset = {}
    num_models = 0
    num_instances = 0
    # count
    for appname in inspect.appnames:
        if appname in EXCLUDE:
            continue
        models = inspect.models(appname)
        if err.exists:
            err.new(get_data, "Can not get models data")
            return
        if len(models) < 1:
            continue
        if models is not None:
            for model in models:
                print("[x] Model", model.__name__)
                try:
                    num = model.objects.all().count()
                except Exception as e:
                    err.new(e)
                    continue
                num_models += 1
                num_instances += num
                dataset[model.__name__] = num
    return dataset


def serialize_app(appname):
    global OK
    dataset = {}
    models = inspect.models(appname)
    if models is None:
        err.new("No model found", serialize_app)
        return
    for model in models:
        try:
            num = model.objects.all().count()
            modelname = model.__name__
            dataset[modelname] = num
            # chart
            x = ("model", "model:N")
            y = ("instances", "instances:Q")
            opts = dict(width=960, height=350)
            c = chart.draw(dataset, x, y, "bar", opts=opts)
            chart.stack(modelname, modelname, c)
            print(OK + "Chart", colors.bold(appname), "saved")
        except ImportError as e:
            err.new(e + " Model not found")
            return


def serialize_models():
    global OK
    print("Serializing models...")
    x_opts = dict(color="model:N", labelAngle=-45, labelPadding=15)
    x = ("model", "model:N", x_opts)
    y = ("number", "number:Q")
    slug = "index"
    title = "All models"
    # get the dataset
    dataset = get_data()
    if err.exists:
        err.report()
    # print(dataset)
    opts = dict(width=1000, height=400)
    c = chart.draw(dataset, x, y, "bar", opts=opts)
    chart.stack(slug, "", c)
    if err.exists:
        err.report()
    print(OK + "Chart", colors.bold(title), "saved")


def run(events=None):
    global EXCLUDE
    chart.engine = "altair"
    serialize_models()
    if err.exists:
        err.report()
    inspect.apps()
    for appname in inspect.appnames:
        if appname not in EXCLUDE:
            serialize_app(appname)
    chart.export("dashboards/chartmodels")
    if err.exists:
        err.report()
