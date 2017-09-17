# Django Chartmodels

Charts and stats for Django models using [Django Chartflo](https://github.com/synw/django-chartflo). Features:

- Chart all apps models
- Chart one app models

## Install

Clone the latest [django-chartflo](https://github.com/synw/django-chartflo) master and install it

Clone this repository and install dependencies: `pip install django-introspection goerr blessings`

Installed apps:


   ```python
   "introspection",
   "django_extensions",
   "chartflo",
   "chartmodels",
   ```
  
Urls:

   ```python
   url('^charts/', include('chartmodels.urls')),
   ```

Generate the charts:

   ```
   python3 manage.py runscript chartmodels
   ```

Go to ``/charts/`` to see it in action. For the users dashboard go to `/charts/users/`

Setting to excude certain models from the charts:

   ```python
   CHARTMODELS_EXCLUDE = ("admin", "mymodel1", "mymodel2")
   ```

## Screenshot

![Models chart](https://raw.github.com/synw/django-chartmodels/master/docs/img/chartall.png)