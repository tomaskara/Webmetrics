from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from speedcheck import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_registration.backends.activation.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", views.home),
    path("", include("dashboard.urls")),
    path("", include("articles.urls")),
    path("profile/", views.profilepage, name="profilepage"),
    path("change-value/", views.change_value, name="change_value"),
    path("delete-annot/", views.delete_annot, name="delete_annot"),
    path("markdownx/", include("markdownx.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
