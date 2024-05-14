import pytest
from common.tests.conftest import user
from django.test import RequestFactory
from influencers.models import BaseProfile
from influencers_statistic.tests.test_models.test_statistics_model import base_profile, valid_statistics_instance_data
from influencers_statistic.views import ProfileStatsUpdater, update_statistic_view


@pytest.fixture
def mock_base_profile_method_create(mocker, user, valid_statistics_instance_data):
    return mocker.patch(
        "influencers.models.BaseProfile.objects.create",
        return_value=BaseProfile(
            pk=valid_statistics_instance_data["profile"]["pk"],
            user=user,
            url_profile=valid_statistics_instance_data["profile"]["url_profile"],
        ),
    )


@pytest.fixture
def mock_profile_stats_updater(mocker):
    return mocker.patch("influencers_statistic.views.ProfileStatsUpdater")


@pytest.fixture
def statistics_method_update_or_create_mock(mocker):
    return mocker.patch("influencers_statistic.models.Statistics.objects.update_or_create")


@pytest.fixture
def mock_client(mocker):
    return mocker.patch("utils.ProfileClient")


@pytest.mark.django_db
def test_profile_stats_updater_add_statistics(
    mocker, mock_base_profile_method_create, valid_statistics_instance_data, mock_profile_stats_updater, mock_client
):
    # Arrange
    profile = BaseProfile.objects.create(**valid_statistics_instance_data["profile"])
    mocker.patch("influencers.models.BaseProfile.objects.get", return_value=profile)

    # Встановлюємо profile_data на тестові дані
    test_updater_instance = mock_profile_stats_updater.return_value
    mock_profile_stats_updater.return_value.profile_data = valid_statistics_instance_data

    ProfileStatsUpdater(profile.pk)

    # Act
    test_updater_instance.add_statistics()

    # Assert
    assert mock_base_profile_method_create.called
    assert mock_profile_stats_updater


@pytest.mark.django_db
def test_update_statistic_view(
    mock_base_profile_method_create,
    statistics_method_update_or_create_mock,
    valid_statistics_instance_data,
    mock_client,
):
    # Arrange
    request = RequestFactory().get("/")
    BaseProfile.objects.create(**valid_statistics_instance_data["profile"])
    mock_client.get_profile_followers.return_value = valid_statistics_instance_data["followers"]
    mock_client.get_profile_photo.return_value = valid_statistics_instance_data["profile_pictures_url"]
    mock_client.get_save_profile_pictures.return_value = valid_statistics_instance_data["profile_pictures"]

    # Act
    response = update_statistic_view(request)

    # Assert
    assert response.status_code == 200
    assert statistics_method_update_or_create_mock.call_count == BaseProfile.objects.count()
