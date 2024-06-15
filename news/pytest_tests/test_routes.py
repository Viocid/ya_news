from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    "reverse_url, parametrized_client, expected_status",
    (
        (
            pytest.lazy_fixture("url_home"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_login"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_logout"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_signup"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_detail"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_edit"),
            pytest.lazy_fixture("author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_delete"),
            pytest.lazy_fixture("author_client"),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture("url_edit"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture("url_delete"),
            pytest.lazy_fixture("not_author_client"),
            HTTPStatus.NOT_FOUND,
        ),
    ),
)
def test_pages_availability_for_anonymous_user(
    reverse_url, parametrized_client, expected_status, news
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "reverse_url",
    (
        pytest.lazy_fixture("url_edit"),
        pytest.lazy_fixture("url_delete"),
    ),
)
def test_redirects(client, url_login, reverse_url):
    expected_url = f"{url_login}?next={reverse_url}"
    response = client.get(reverse_url)
    assertRedirects(response, expected_url)
