"""User url routes"""
from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from users.views import (
    ChangeEmailRequestViewSet,
    CountriesStatesViewSet,
    CurrentUserRetrieveUpdateViewSet,
    UserRetrieveViewSet,
    UsersViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserRetrieveViewSet, basename="users_api")
router.register(r"countries", CountriesStatesViewSet, basename="countries_api")
router.register(
    r"change-emails", ChangeEmailRequestViewSet, basename="change_email_api"
)
router.register(r"user_search", UsersViewSet, basename="users_search_api")

urlpatterns = [
    path(
        "api/users/me",
        CurrentUserRetrieveUpdateViewSet.as_view(
            {"patch": "update", "get": "retrieve"}
        ),
        name="users_api-me",
    ),
    path("api/", include(router.urls)),
]
