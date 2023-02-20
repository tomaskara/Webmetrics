from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from dashboard.views import dashboard


urlpatterns = [
    path('dashboard/<int:url_id>/', dashboard, name='dashboard'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()