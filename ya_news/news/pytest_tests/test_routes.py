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
    'url, client_fixture, expected_status, redirect_url',
    (
        (EDIT, AUTHOR, OK, None),
        (DELETE, AUTHOR, OK, None),
        (EDIT, AUTH_USER, NOT_FOUND, None),
        (DELETE, AUTH_USER, NOT_FOUND, None),
        (HOME, ANONIMOUS, OK, None),
        (DETAIL, ANONIMOUS, OK, None),
        (LOGIN, ANONIMOUS, OK, None),
        (LOGOUT, ANONIMOUS, OK, None),
        (SIGNUP, ANONIMOUS, OK, None),
        (EDIT, ANONIMOUS, FOUND, REDIRECT_EDIT),
        (DELETE, ANONIMOUS, FOUND, REDIRECT_DELETE),
    )
)
def test_page_availability_and_redirects(url, client_fixture,
                                         expected_status, redirect_url):
    response = client_fixture.get(url)
    assert response.status_code == expected_status
    if redirect_url:
        assertRedirects(response, redirect_url)
