import pytest
from common.tests.conftest import client, user
from django.urls import reverse
from influencers_statistic.statistics_services import InfluencersStatisticsServices


@pytest.mark.parametrize(
    "period",
    [
        "last_7_days",
        "last_90_days",
        "",
    ],
)
@pytest.mark.django_db
def test_period_statistic_view(client, user, period):
    client.force_login(user)

    url = reverse("period_statistics")
    response = client.get(url, {"period": period})

    assert response.status_code == 200
    assert "influencers_statistic/period_statistics.html" in response.template_name

    assert "statistics_period" in response.context_data
    assert "date_start" in response.context_data
    assert "date_end" in response.context_data
    assert "period" in response.context_data
    assert response.context_data["title"] == "Filter by period statistics"


@pytest.mark.django_db
def test_anonymous_user_redirect(client):
    # Відправлення запиту без авторизації
    url = reverse("period_statistics")
    response = client.get(url)

    # Перевірка, що анонімні користувачі перенаправляються на сторінку входу
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/influencers_statistic/period_statistics/"


@pytest.mark.parametrize(
    "date_start, date_end, expected_result",
    [
        ("2024-04-22", "2024-04-20", []),
    ],
)
def test_validate_dates(date_start, date_end, expected_result):
    result = list(InfluencersStatisticsServices.validate_dates(date_start, date_end))
    assert result == expected_result
