import pytest
from common.tests.conftest import client, user
from django.urls import reverse


@pytest.mark.parametrize(
    "sort_by, order",
    [
        ("followers", "asc"),
        ("created_at", "desc"),
        ("", ""),
    ],
)
@pytest.mark.django_db
def test_base_statistic_view(client, user, sort_by, order):
    client.force_login(user)

    url = reverse("statistics")
    response = client.get(url, {"sort_by": sort_by, "order": order})

    assert response.status_code == 200
    assert "influencers_statistic/statistics.html" in response.template_name

    assert "statistics" in response.context_data
    assert "sort_by" in response.context_data
    assert "order" in response.context_data


@pytest.mark.django_db
def test_anonymous_user_redirect(client):
    # Відправлення запиту без авторизації
    url = reverse("statistics")
    response = client.get(url)

    # Перевірка, що анонімні користувачі перенаправляються на сторінку входу
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/influencers_statistic/statistics/"
