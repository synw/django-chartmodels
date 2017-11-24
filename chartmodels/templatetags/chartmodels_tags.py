# -*- coding: utf-8 -*-

from django import template
from introspection.inspector import inspect
from chartmodels.conf import EXCLUDE


register = template.Library()


@register.simple_tag
def modelnames():
    models = []
    for appname in inspect.appnames:
        if appname in EXCLUDE:
            continue
        models.append(inspect.models(appname))
    names = []
    for model in models:
        for submod in model:
            names.append(submod.__name__)
    return names
