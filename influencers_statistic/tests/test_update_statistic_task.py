import pytest
from common.tests.conftest import base_profile, user, valid_statistics_instance_data
from influencers.models import BaseProfile
from influencers_statistic.tasks import update_statistic


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
def mock_logger(mocker):
    return mocker.patch("influencers_statistic.tasks.logger")


@pytest.fixture
def mock_time(mocker):
    return mocker.patch("influencers_statistic.tasks.time")


@pytest.mark.django_db
def test_update_statistic_success(mocker, mock_logger, mock_time, user):
    # Arrange
    mock_base_profile_all = mocker.patch("influencers.models.BaseProfile.objects.all")
    mock_base_profile_all.return_value = []

    # Act
    update_statistic()

    # Assert
    assert mock_logger.info.call_count == 1
    assert mock_logger.error.call_count == 0
    assert mock_logger.info.call_args_list[0][0][0] == "Statistics successfully updated for all profiles."

    # Check time.sleep call
    assert mock_time.sleep.called_once_with(10)


@pytest.mark.django_db
def test_update_statistic_failure(mocker, mock_base_profile_method_create, mock_logger, user):
    # Arrange
    mock_base_profile_all = mocker.patch("influencers.models.BaseProfile.objects.all")
    mock_base_profile_all.return_value = Exception()

    # Act & Assert
    with pytest.raises(Exception):
        update_statistic()

    assert mock_logger.info.call_count == 0
    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args_list[0][0][0] == "Exceptional case, retry in 5 seconds."
