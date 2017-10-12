# -*- coding: utf-8 -*-

from __future__ import print_function
from introspection.inspector import inspect
from blessings import Terminal
from goerr import err
from chartflo.factory import ChartController
from chartflo.models import Chart
from chartmodels.conf import EXCLUDE


color = Terminal()
OK = "[" + color.bold_green("ok") + "] "


def get_data():
    dataset = {}
    num_models = 0
    num_instances = 0
    # count
    for appname in inspect.appnames:
        if appname in EXCLUDE:
            continue
        models = inspect.models(appname)
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
    dataset = {}
    models = inspect.models(appname)
    if models is None:
        err.new("No model found", serialize_app)
        return
    for model in models:
        try:
            num = model.objects.all().count()
            dataset[model.__name__] = num
        except ImportError as e:
            err.new(e + " Model not found")
    # chart
    chart = ChartController()
    chart_type = "bar"
    x = ("model", "model:N")
    y = ("instances", "instances:Q")
    width = 960
    height = 350
    slug = "app_" + appname
    name = "App " + appname
    chart.generate(slug, name, chart_type,
                   dataset, x, y, width=width, height=height,
                   generator="chartmodels.users", color="model:N")
    print(OK + "Chart", color.bold(slug), "saved")


def serialize_models():
    global OK
    print("Serializing models...")
    chart_type = "bar"
    x = ("model", "model:N")
    y = ("number", "number:Q")
    width = 1000
    height = 500
    slug = "all_models"
    name = ""
    # get the dataset
    dataset = get_data()
    # print(dataset)
    chart = ChartController()
    chart.generate(slug, name, chart_type,
                   dataset, x, y, width=width, height=height,
                   generator="chartmodels.users", color="model:N")
    print(OK + "Chart", color.bold(slug), "saved")


def run(events):
    global EXCLUDE
    serialize_models()
    if err.exists:
        err.report()
    inspect.apps()
    for appname in inspect.appnames:
        if appname not in EXCLUDE:
            serialize_app(appname)
    if err.exists:
        err.report()
