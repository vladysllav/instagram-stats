import pytest
from common.tests.conftest import client
from django.contrib.auth import logout
from django.urls import reverse


@pytest.mark.django_db
def test_valid_logout_view(client):
    # Перевірка, що користувач вийшов з системи після виконання POST-запиту на вихід
    data = {
        "username": "testuser",
        "password": "StrongPassword123",
    }
    response = client.post(reverse("logout"), data)

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_user_is_not_authenticated(client):
    # Перевірка, що користувач більше не аутентифікований після виходу
    logout(client)

    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session
