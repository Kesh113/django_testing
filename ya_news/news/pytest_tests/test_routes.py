from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None))
)
def test_pages_availability_for_anonymous_user(client, name, args):
    response = client.get(reverse(name, args=args))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('auth_user_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('edit', 'delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, expected_status, name, urls_for_comment):
    response = parametrized_client.get(urls_for_comment[name])
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('edit', 'delete')
)
def test_redirects(client, name, urls_for_comment):
    url = urls_for_comment[name]
    assertRedirects(client.get(url), f'{reverse("users:login")}?next={url}')
