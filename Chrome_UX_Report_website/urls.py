from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from speedcheck import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_registration.backends.activation.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", views.home),
    path("", include("dashboard.urls")),
    path("", include("articles.urls")),
    path("", include("utm_generator.urls")),
    path("profile/", views.profilepage, name="profilepage"),
    path("change-value/", views.change_value, name="change_value"),
    path("delete-annot/", views.delete_annot, name="delete_annot"),
    path("markdownx/", include("markdownx.urls")),
    path("user/", views.userpage, name="userpage"),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('test-page/', views.test_page, name="test_page"),
    path('tools/', views.tools, name="tools")
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
