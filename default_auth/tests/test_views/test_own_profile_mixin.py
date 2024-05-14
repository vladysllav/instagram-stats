import pytest
from common.tests.conftest import base_profile, client, user
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def own_profile_mixin_method_get_object_mock(mocker):
    return mocker.patch("default_auth.views.OwnProfileMixin.get_object")


@pytest.fixture
def other_user():
    return User.objects.create_user(username="testuser2", email="testuser2@example.com", password="StrongPassword1234")


@pytest.fixture
def other_base_profile(other_user):
    return {
        "pk": 2,
        "user": other_user,
        "url_profile": "https://www.instagram.com/testuser2/",
    }


@pytest.mark.django_db
def test_get_object_own_profile(client, user, base_profile, own_profile_mixin_method_get_object_mock):
    client.force_login(user)
    response = client.get(reverse("profile_detail", kwargs={"pk": base_profile["pk"]}))
    assert response.status_code == 200
    assert response.context["user"] == user

    assert own_profile_mixin_method_get_object_mock.called_with(pk=base_profile["pk"])


@pytest.mark.django_db
def test_get_object_other_profile(client, user, other_base_profile):
    client.force_login(user)
    response = client.get(reverse("profile_detail", kwargs={"pk": other_base_profile["pk"]}))
    assert response.status_code == 404
