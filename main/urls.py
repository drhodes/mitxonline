"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from oauth2_provider.urls import base_urlpatterns

from main.views import index

urlpatterns = [
    # NOTE: we only bring in base_urlpatterns so applications can only be created via django-admin
    path(
        "oauth2/",
        include((base_urlpatterns, "oauth2_provider"), namespace="oauth2_provider"),
    ),
    path("admin/", admin.site.urls),
    path("status/", include("server_status.urls")),
    path("hijack/", include("hijack.urls")),
    path("robots.txt", include("robots.urls")),
    path("", include("authentication.urls")),
    path("", include("openedx.urls")),
    path("", include("mail.urls")),
    path("", include("users.urls")),
    # social django needs to be here to preempt the login
    path("", include("social_django.urls", namespace="social")),
    # Example view
    path("", index, name="main-index"),
    path("signin/", index, name="login"),
    path("signin/password/", index, name="login-password"),
    re_path(r"^signin/forgot-password/$", index, name="password-reset"),
    re_path(
        r"^signin/forgot-password/confirm/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        index,
        name="password-reset-confirm",
    ),
    path("create-account/", index, name="signup"),
    path("create-account/details/", index, name="signup-details"),
    path("create-account/extra/", index, name="signup-extra"),
    path("create-account/denied/", index, name="signup-denied"),
    path("create-account/error/", index, name="signup-error"),
    path("create-account/confirm/", index, name="register-confirm"),
    path("account/inactive/", index, name="account-inactive"),
    path("account/confirm-email/", index, name="account-confirm-email-change"),
    re_path(r"^account-settings/", index, name="account-settings"),
]

if settings.DEBUG:
    import debug_toolbar  # pylint: disable=wrong-import-position, wrong-import-order

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
