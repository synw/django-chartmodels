# -*- coding: utf-8 -*-

from __future__ import print_function
from introspection.inspector import inspect
from blessings import Terminal
from goerr import err
from chartflo.factory import ChartController
from chartflo.models import Chart
from chartmodels.conf import EXCLUDE
from .users import generate_users


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
        models, err = inspect.models(appname)
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
    return dataset, err


def serialize_app(appname):
    dataset = {}
    models, err = inspect.models(appname)
    if models is None:
        return err
    if err.exists:
        err.trace()
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
    datapack = chart.serialize_count(
        dataset, x, y, chart_type=chart_type, width=width, height=height, color="model:N")
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.generate(chart, slug, name, datapack)
    print(OK + "Chart", color.bold(slug), "saved")
    return err


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
    dataset, err = get_data()
    # print(dataset)
    chart = ChartController()
    datapack = chart.serialize_count(
        dataset, x, y, chart_type=chart_type, width=width, height=height, color="model:N")
    chart, _ = Chart.objects.get_or_create(slug=slug)
    chart.generate(chart, slug, name, datapack)
    print(OK + "Chart", color.bold(slug), "saved")
    return err


def run(events):
    global EXCLUDE
    err = serialize_models()
    if err.exists:
        err.trace()
    inspect.apps()
    for appname in inspect.appnames:
        if appname not in EXCLUDE:
            err = serialize_app(appname)
    generate_users()
    if err.exists:
        err.trace()
