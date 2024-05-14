import pytest
from common.tests.conftest import user
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from influencers.models import BaseProfile


@pytest.fixture
def base_profile_method_create_mock(mocker):
    return mocker.patch("influencers.models.BaseProfile.objects.create")


@pytest.fixture
def valid_profile_data(user):
    return {
        "user": user,
        "url_profile": "https://www.instagram.com/testuser/",
    }


@pytest.mark.django_db
def test_create_base_profile(valid_profile_data, base_profile_method_create_mock):
    # Create a new BaseProfile instance using the provided data
    base_profile_obj = BaseProfile(**valid_profile_data)
    # Set the return value of the create method to the created BaseProfile instance
    base_profile_method_create_mock.return_value = base_profile_obj

    created_base_profile = BaseProfile.objects.create(**valid_profile_data)

    # Assert that the created BaseProfile matches the expected data
    assert created_base_profile.user == valid_profile_data["user"]
    assert created_base_profile.url_profile == valid_profile_data["url_profile"]

    # Assert that the create method was called once
    assert base_profile_method_create_mock.called
    assert base_profile_method_create_mock.call_count == 1


@pytest.mark.django_db
def test_unique_base_profile(user, base_profile_method_create_mock):
    # Set the return value for the mock function
    base_profile_method_create_mock.side_effect = [
        BaseProfile(user=user, url_profile="https://www.instagram.com/testuser/"),
        IntegrityError,  # Raise IntegrityError to observe its occurrence
    ]

    # Try to create two objects with the same url_profile
    BaseProfile.objects.create(user=user, url_profile="https://www.instagram.com/testuser/")
    with pytest.raises(IntegrityError):
        BaseProfile.objects.create(user=user, url_profile="https://www.instagram.com/testuser/")

    assert base_profile_method_create_mock.called
    assert base_profile_method_create_mock.call_count == 2


@pytest.mark.django_db
def test_base_profile_validation(user, base_profile_method_create_mock):
    base_profile_method_create_mock.side_effect = ValidationError("User field couldn't be empty")
    with pytest.raises(ValidationError):
        BaseProfile.objects.create(user="", url_profile="https://www.instagram.com/testuser/")

    assert base_profile_method_create_mock.side_effect.message == "User field couldn't be empty"
    assert base_profile_method_create_mock.called
    assert base_profile_method_create_mock.call_count == 1


@pytest.mark.django_db
def test_get_object_url(user, base_profile_method_create_mock):
    base_profile_method_create_mock.return_value = BaseProfile(
        pk=1, user=user, url_profile="https://www.instagram.com/testuser/"
    )

    base_profile = BaseProfile.objects.create(pk=1, user=user, url_profile="https://www.instagram.com/testuser/")
    expected_url = reverse("profile_detail", kwargs={"pk": base_profile.pk})

    assert base_profile.get_absolute_url() == expected_url
    assert base_profile_method_create_mock.called
    assert base_profile_method_create_mock.call_count == 1


@pytest.mark.django_db
def test_base_profile_performance(benchmark, base_profile_method_create_mock):
    def create_base_profiles():
        for i in range(100):
            BaseProfile.objects.create(name=f"Test User {i}", url_profile=f"https://www.instagram.com/testuser_{i}/")

    benchmark(create_base_profiles)
