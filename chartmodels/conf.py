# -*- coding: utf-8 -*-

from django.conf import settings


EXCLUDE = getattr(settings, 'CHARTMODELS_EXCLUDE', ["admin", "filebrowser"])