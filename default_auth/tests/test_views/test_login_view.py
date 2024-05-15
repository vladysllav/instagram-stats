import pytest
from common.tests.conftest import client, user
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_valid_login_view(client, user):
    # Перевірка, що користувач може успішно автентифікуватися з правильними даними
    data = {
        "username": "testuser",
        "password": "StrongPassword123",
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 302
    assert response.url == reverse("home")

    # Перевірка, що користувач автентифікований після успішного логіну
    assert "_auth_user_id" in response.client.session
    assert response.client.session["_auth_user_id"] == str(user.pk)

    # Перевірка атрибутів об'єкту користувача
    user_obj = User.objects.get(username="testuser")
    assert user_obj.is_authenticated
    assert user_obj.is_active
    assert user_obj.is_staff is False


@pytest.mark.django_db
def test_invalid_login_view(client, user):
    # Перевірка, що користувач не може автентифікуватися з неправильними даними
    data = {
        "username": "testuser",
        "password": "WrongPassword123",  # Неправильний пароль
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 200
    assert response.context["user"].is_authenticated is False
    assert "Wrong credentials. Please try again with correct input" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_invalid_form_login_view(client, user):
    # Перевірка, що користувач не може автентифікуватися з неправильними даними форми
    data = {
        "username": "",  # Пусте поле
        "password": "",  # Пусте поле
    }
    response = client.post(reverse("login"), data)

    assert response.status_code == 200
    assert response.context["user"].is_authenticated is False
    assert "Please correct the errors below." in response.content.decode("utf-8")
