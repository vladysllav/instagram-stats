import pytest
from default_auth.forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_invalid_signup_form():
    # Перевірка валідації форми з неправильними даними
    form_data = {
        "username": "User123",
        "password": "",
    }

    form = LoginForm(data=form_data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_valid_login_form():
    # Перевірка валідації форми з правильними даними
    form_data = {
        "username": "User123",
        "password": "value1324",
    }
    form = LoginForm(data=form_data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_invalid_login():
    # Перевірка невдалих спроб входу з неправильними даними
    User.objects.create_user(username="testuser", password="correctpassword")
    login_data = {"username": "testuser", "password": "wrongpassword"}
    form = LoginForm(data=login_data)
    assert form.is_valid() is True
    assert authenticate(username=login_data["username"], password=login_data["password"]) is None


@pytest.mark.django_db
def test_valid_login():
    # Перевірка правильного входу з вірними даними
    User.objects.create_user(username="testuser", password="correctpassword")
    login_data = {"username": "testuser", "password": "correctpassword"}
    form = LoginForm(data=login_data)
    assert form.is_valid() is True
    assert authenticate(username=login_data["username"], password=login_data["password"]) is not None
