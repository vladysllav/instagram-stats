import pytest
from influencers.forms import ProfileForm


@pytest.fixture
def valid_profile_form_data():
    return {
        "url_profile": "https://www.instagram.com/testuser/",
    }


@pytest.mark.django_db
def test_invalid_profile_form():
    # Перевірка валідації форми з неправильними даними
    form_data = {
        "url_profile": 123,
    }

    form = ProfileForm(data=form_data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_valid_profile_form(valid_profile_form_data):
    # Перевірка валідації форми з правильними даними
    form = ProfileForm(data=valid_profile_form_data)
    assert form.is_valid() is True
    assert form.cleaned_data["url_profile"] == valid_profile_form_data["url_profile"]
