from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db

EDIT = pytest.lazy_fixture('edit')
DELETE = pytest.lazy_fixture('delete')

ANONIMOUS = pytest.lazy_fixture('client')
AUTH_USER = pytest.lazy_fixture('auth_user_client')
AUTHOR = pytest.lazy_fixture('author_client')

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    (
        (EDIT, AUTH_USER, NOT_FOUND),
        (EDIT, AUTHOR, OK),
        (DELETE, AUTH_USER, NOT_FOUND),
        (DELETE, AUTHOR, OK),
        (pytest.lazy_fixture('home'), ANONIMOUS, OK),
        (pytest.lazy_fixture('detail'), ANONIMOUS, OK),
        (pytest.lazy_fixture('login'), ANONIMOUS, OK),
        (pytest.lazy_fixture('logout'), ANONIMOUS, OK),
        (pytest.lazy_fixture('signup'), ANONIMOUS, OK)
    )
)
def test_pages_availability_for_different_users(url, client_fixture,
                                                expected_status, ):
    response = client_fixture.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (EDIT, DELETE)
)
def test_redirects(client, url, login):
    assertRedirects(client.get(url), f'{login}?next={url}')
