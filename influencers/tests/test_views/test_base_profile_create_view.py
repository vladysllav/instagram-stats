import pytest
from common.tests.conftest import client, user
from django.http import HttpResponseRedirect
from django.urls import reverse
from influencers.models import BaseProfile


@pytest.fixture
def base_profile_form_valid_mock(mocker):
    return mocker.patch(
        "influencers.views.BaseProfileCreateView.form_valid",
        side_effect=[HttpResponseRedirect("/influencers/profiles/1/")],
    )


@pytest.mark.django_db
def test_base_profile_views(client, user, base_profile_form_valid_mock):
    client.force_login(user)
    # Arrange
    data = {
        "user": user,
        "url_profile": "https://www.instagram.com/testuser/",
    }

    response = client.post(reverse("profile_create"), data=data)
    assert response.status_code == 302
    assert response.url == "/influencers/profiles/1/"

    assert base_profile_form_valid_mock.called

    created_profile = BaseProfile(user=user, url_profile="https://www.instagram.com/testuser/")
    assert created_profile.url_profile == data["url_profile"]
    assert created_profile.user == user


@pytest.mark.django_db
def test_base_profile_create_view_unauthenticated_user(client):
    # Спроба доступу до сторінки створення профілю без автентифікації
    response = client.get(reverse("profile_create"))

    # Перевірка, що користувач був перенаправлений на сторінку входу
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/influencers/profiles/"
