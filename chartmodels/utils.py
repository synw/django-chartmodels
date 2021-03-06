from __future__ import print_function
import importlib
from django.conf import settings
from django.apps import apps


def get_model_from_path(modpath):
    modsplit = modpath.split('.')
    path = '.'.join(modsplit[:-1])
    modname = '.'.join(modsplit[-1:])
    module = importlib.import_module(path)
    model = getattr(module, modname)
    return model


def get_all_models(appname, names_only=False):
    models = []
    if '.' in appname:
        s = appname.split('.')
        appname = s[-1:][0]
    try:
        mods = apps.get_app_config(appname).get_models()
        for model in mods:
            if names_only is True:
                models.append(model.__name__)
            else:
                models.append(model)
    except:
        print(str(appname) + " models not found ")
    return models


def get_all_apps_models(names_only=False):
    allmodels = {}
    for appname in settings.INSTALLED_APPS:
        models = get_all_models(appname, names_only)
        if "." in appname:
            s = appname.split(".")
            m = len(s) - 1
            appname = s[m:][0]
        allmodels[appname] = sorted(models)
    return allmodels
