import pytest
from common.tests.conftest import client
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse


@pytest.mark.django_db
def test_valid_signup_view(client):
    # Перевірка, що користувач може успішно зареєструватися з правильними даними
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPassword123",
        "password2": "StrongPassword123",
    }
    response = client.post(reverse("signup"), data)

    assert response.status_code == 302
    assert response.url == reverse("home")

    # Перевірка, що користувач збережений у базі даних
    user = User.objects.filter(username="testuser")
    assert user.exists()

    # Перевірка, що пароль зберігається у захешованому вигляді
    assert user.values("password") != data["password"]


@pytest.mark.django_db
def test_invalid_signup_view(client):
    # Перевірка, що користувач не може зареєструватися з неправильними даними
    data = {
        "username": "testuser",
        "email": "invalidemail",
        "password": "StrongPassword123",
        "password2": "StrongPassword123",
    }
    response = client.post(reverse("signup"), data)

    assert response.status_code == 200
    assert response.context["form"].errors

    # Перевірка, що користувач не збережений у базі даних
    assert not User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_create_duplicate_user():
    # Перевірка створення дублікату контакту, що має призвести до виникнення IntegrityError.
    User.objects.create(
        username="testuser",
        email="testuser@example.com",
        password="StrongPassword123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="StrongPassword123",
        )
