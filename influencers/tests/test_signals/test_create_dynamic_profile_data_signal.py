import pytest
from django.contrib.auth.models import User
from influencers.models import BaseProfile
from influencers_statistic.models import Statistics


@pytest.fixture
def mocked_client(mocker):
    mocked = mocker.patch("influencers.signals.client")
    mocked.get_save_profile_pictures.return_value = "profile_pictures_data"
    mocked.get_profile_followers.return_value = 1000
    mocked.get_profile_photo.return_value = "profile_photo_url"
    yield mocked


@pytest.mark.django_db
def test_create_dynamic_profile_data(mocked_client):
    # Створюємо користувача
    user = User.objects.create(username="testuser")

    # Створюємо екземпляр BaseProfile
    base_profile = BaseProfile.objects.create(user=user, url_profile="https://www.instagram.com/testuser/")

    # Перевіряємо, що Statistics було створено з правильними даними
    statistics = Statistics.objects.get(profile=base_profile)
    assert statistics.profile == base_profile
    assert statistics.name == base_profile.url_profile.rstrip("/").split("/")[-1]
    assert statistics.profile_pictures == "profile_pictures_data"
    assert statistics.followers == 1000
    assert statistics.profile_pictures_url == "profile_photo_url"
