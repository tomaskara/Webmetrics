from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from utm_generator.views import utm_builder

urlpatterns = [
    path("utm_generator/", utm_builder, name="utm_generator"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
