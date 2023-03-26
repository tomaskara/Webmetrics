from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from dashboard.views import dashboard, remove_profile_url, add_profile_url
from speedcheck.views import change_value


urlpatterns = [
    path('dashboard/<int:url_id>/', dashboard, name='dashboard'),
    path('remove-value/', remove_profile_url, name='remove_value'),
    path('add-value/', add_profile_url, name='add_value'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()