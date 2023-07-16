from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from articles.views import article_detail, article_list


urlpatterns = [
    path("articles/<slug>/", article_detail, name="article_detail"),
    path("articles/", article_list, name="article_list"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
