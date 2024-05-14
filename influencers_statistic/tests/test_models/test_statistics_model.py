import pytest
from common.tests.conftest import base_profile, user, valid_statistics_instance_data
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from influencers.models import BaseProfile
from influencers_statistic.models import Statistics


@pytest.fixture
def statistics_method_create_mock(mocker):
    return mocker.patch("influencers_statistic.models.Statistics.objects.create")


@pytest.fixture
def base_profile_method_create_mock(mocker, user, valid_statistics_instance_data):
    return mocker.patch(
        "influencers.models.BaseProfile.objects.create",
        return_value=BaseProfile(user=user, url_profile=valid_statistics_instance_data["profile"]["url_profile"]),
    )


@pytest.mark.django_db
def test_create_statistics_instance(
    valid_statistics_instance_data, base_profile, statistics_method_create_mock, base_profile_method_create_mock, user
):
    # Створення екземпляра BaseProfile
    created_base_profile_instance = BaseProfile.objects.create(**base_profile)

    # Заміна значення profile в valid_statistics_instance_data на екземпляр BaseProfile
    valid_statistics_instance_data["profile"] = created_base_profile_instance

    # Модифікація моку для повернення об'єкта Statistics замість патча
    statistics_obj = Statistics(**valid_statistics_instance_data)
    statistics_method_create_mock.return_value = statistics_obj

    # Створення екземпляра Statistics
    created_statistics_instance = Statistics.objects.create(**valid_statistics_instance_data)

    # Перевірка, що створений об'єкт Statistics містить очікувані дані
    assert created_statistics_instance.profile == valid_statistics_instance_data["profile"]
    assert created_statistics_instance.name == valid_statistics_instance_data["name"]
    assert created_statistics_instance.profile_pictures == valid_statistics_instance_data["profile_pictures"]
    assert created_statistics_instance.profile_pictures_url == valid_statistics_instance_data["profile_pictures_url"]
    assert created_statistics_instance.followers == valid_statistics_instance_data["followers"]

    # Перевірка, що метод create викликався один раз
    assert statistics_method_create_mock.called
    assert statistics_method_create_mock.call_count == 1
    assert base_profile_method_create_mock.call_count == 1


@pytest.mark.django_db
def test_statistics_validation(user, statistics_method_create_mock):
    statistics_method_create_mock.side_effect = ValidationError("Profile field couldn't be empty")
    with pytest.raises(ValidationError):
        Statistics.objects.create(profile="", name="testuser")

    assert statistics_method_create_mock.side_effect.message == "Profile field couldn't be empty"
    assert statistics_method_create_mock.called
    assert statistics_method_create_mock.call_count == 1


@pytest.mark.django_db
def test_unique_statistics(user, base_profile, base_profile_method_create_mock, statistics_method_create_mock):
    base_profile_obj = BaseProfile.objects.create(**base_profile)
    # Set the return value for the mock function
    statistics_method_create_mock.side_effect = [
        Statistics(profile=base_profile_obj, name="testuser"),
        IntegrityError,  # Raise IntegrityError to observe its occurrence
    ]

    # Try to create two objects with the same url_profile
    Statistics.objects.create(profile=base_profile_obj, name="testuser")
    with pytest.raises(IntegrityError):
        Statistics.objects.create(profile=base_profile_obj, name="testuser")

    assert statistics_method_create_mock.called
    assert statistics_method_create_mock.call_count == 2


def test_statistics_model_string_representation():
    # Створюємо екземпляр Statistics з певним ім'ям
    statistics_instance = Statistics(name="Test Name")

    # Перевіряємо, що метод __str__ повертає очікуваний рядок
    assert str(statistics_instance) == "Statistics for Test Name"


def test_statistics_model_string_representation_without_name():
    # Створюємо екземпляр Statistics без імені
    statistics_instance = Statistics()

    # Перевіряємо, що метод __str__ повертає рядок за замовчуванням
    assert str(statistics_instance) == "Statistics for None"


@pytest.mark.django_db
def test_get_start_end_statistics(
    user,
    base_profile,
    valid_statistics_instance_data,
    base_profile_method_create_mock,
    statistics_method_create_mock,
    mocker,
):
    # Створення тестового профілю
    created_base_profile_instance = BaseProfile.objects.create(**base_profile)

    valid_statistics_instance_data["profile"] = created_base_profile_instance

    # Створення тестового об'єкта Statistics
    date_start = timezone.now().date() - timezone.timedelta(days=7)
    date_end = timezone.now().date()
    valid_statistics_instance_data["created_at"] = timezone.now() - timezone.timedelta(days=7)
    statistics_obj = Statistics(**valid_statistics_instance_data)
    statistics_method_create_mock.return_value = statistics_obj

    # Створення екземпляра Statistics
    created_statistics_instance = Statistics.objects.create(**valid_statistics_instance_data)

    mocker.patch.object(
        Statistics.stats_manager, "get_start_end_statistics", return_value=[created_statistics_instance]
    )

    # Отримання результатів від менеджера
    queryset = Statistics.stats_manager.get_start_end_statistics(user, date_start, date_end)

    # Перевірка, що об'єкт Statistics знайдено в результаті
    assert created_statistics_instance in queryset
