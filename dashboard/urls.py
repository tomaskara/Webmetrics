from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from dashboard.views import add_profile_url, dashboard, remove_profile_url, lighthouse_on

urlpatterns = [
    path("dashboard/<int:url_id>/", dashboard, name="dashboard"),
    path("remove-value/", remove_profile_url, name="remove_value"),
    path("add-value/", add_profile_url, name="add_value"),
    path("function/", add_profile_url, name="add_value"),
    path("lighthouse/", lighthouse_on, name="lighthouse_on"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
