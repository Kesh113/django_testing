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
        (EDIT, ANONIMOUS, FOUND),
        (DELETE, ANONIMOUS, FOUND),
        (LOGIN, ANONIMOUS, OK),
        (LOGOUT, ANONIMOUS, OK),
        (SIGNUP, ANONIMOUS, OK)
    )
)
def test_pages_availability_for_different_users(url, client_fixture, client,
                                                expected_status, redirect,
                                                edit, delete):
    assert client_fixture.get(url).status_code == expected_status
    if url in (edit, delete) and client_fixture == client:
        assertRedirects(client_fixture.get(url), f'{redirect}{url}')
