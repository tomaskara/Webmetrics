from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.shortcuts import redirect

from utm_generator.views import utm_builder, utm_builder_redirect

urlpatterns = [
    path("utm_generator/", utm_builder_redirect, name='utm_generator_redirect'),
    path("utm-generator/", utm_builder, name="utm_generator"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
