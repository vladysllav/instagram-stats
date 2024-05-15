import pytest
from django.contrib.auth import get_user_model
from django.test import Client


User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="StrongPassword123")


@pytest.fixture
def base_profile(user):
    return {
        "pk": 1,
        "user": user,
        "url_profile": "https://www.instagram.com/testuser/",
    }


@pytest.fixture
def valid_statistics_instance_data(base_profile):
    return {
        "profile": base_profile,
        "name": "test_user",
        "profile_pictures": "influencers/profile_images/test_user.jpg",
        "profile_pictures_url": "https://test_user_url/",
        "followers": 38732,
    }
