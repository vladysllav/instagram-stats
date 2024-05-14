import pytest
from django.test import RequestFactory
from django.utils.safestring import mark_safe
from influencers_statistic.templatetags.influencers_statistic_tags import sort_link


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.mark.parametrize(
    "label, sort_by_param, current_sort_by, current_order, expected_result",
    [
        (
            "Label",
            "param",
            "other_param",
            "asc",
            '<a href="?sort_by=param&order=desc" style="color: inherit;">Label <i class="fa-solid fa-sort"></i></a>',
        ),
        (
            "Label",
            "param",
            "param",
            "asc",
            '<a href="?sort_by=param&order=desc" style="color: inherit;">Label <i class="fas fa-caret-up"></i></a>',
        ),
        (
            "Label",
            "param",
            "param",
            "desc",
            '<a href="?sort_by=param&order=asc" style="color: inherit;">Label <i class="fas fa-caret-down"></i></a>',
        ),
    ],
)
@pytest.mark.django_db
def test_sort_link_tag(rf, label, sort_by_param, current_sort_by, current_order, expected_result):
    rendered_link = sort_link(label, sort_by_param, current_sort_by, current_order)
    assert rendered_link == mark_safe(expected_result)
