from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db

HOME = pytest.lazy_fixture('home')
DETAIL = pytest.lazy_fixture('detail')
LOGIN = pytest.lazy_fixture('login')
LOGOUT = pytest.lazy_fixture('logout')
SIGNUP = pytest.lazy_fixture('signup')
EDIT = pytest.lazy_fixture('edit')
DELETE = pytest.lazy_fixture('delete')
REDIRECT_EDIT = pytest.lazy_fixture('redirect_edit')
REDIRECT_DELETE = pytest.lazy_fixture('redirect_delete')

ANONIMOUS = pytest.lazy_fixture('client')
AUTH_USER = pytest.lazy_fixture('auth_user_client')
AUTHOR = pytest.lazy_fixture('author_client')

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    (
        (EDIT, AUTHOR, OK),
        (DELETE, AUTHOR, OK),
        (EDIT, AUTH_USER, NOT_FOUND),
        (DELETE, AUTH_USER, NOT_FOUND),
        (HOME, ANONIMOUS, OK),
        (DETAIL, ANONIMOUS, OK),
        (LOGIN, ANONIMOUS, OK),
        (LOGOUT, ANONIMOUS, OK),
        (SIGNUP, ANONIMOUS, OK)
    )
)
def test_pages_availability_for_different_users(url, client_fixture,
                                                expected_status):
    assert client_fixture.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url',
    (
        (EDIT, REDIRECT_EDIT),
        (DELETE, REDIRECT_DELETE),
    )
)
def test_redirects(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url)
