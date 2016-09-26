# Django Chartmodels

Charts and stats for Django models. Features:

- Chart all apps models
- Chart one app models

## Install

  ```bash
pip install git+https://github.com/synw/django-chartflo.git
pip install git+https://github.com/synw/django-chartmodels.git
  ```

Installed apps:


  ```python
'chartflo',
'chartmodels',
  ```
  
Urls:

  ```python
url('^chartflo/', include('chartmodels.urls')),
url('^charts/', include('chartmodels.urls')),
  ```
  
Go to ``/charts/`` to see it in action.

## Screenshot

![Models chart](https://raw.github.com/synw/django-chartmodels/master/docs/img/chartall.png)