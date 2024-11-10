from http import HTTPStatus

from .fixtures import (TestBaseCase, ADD, DETAIL, LIST, SUCCESS, EDIT, DELETE,
                       HOME, LOGIN, LOGOUT, SIGNUP, REDIRECT)


OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
FOUND = HTTPStatus.FOUND


class TestRoutes(TestBaseCase):
    def test_pages_availability(self):
        test_data = (
            (HOME, self.client, OK),
            (LOGIN, self.client, OK),
            (LOGOUT, self.client, OK),
            (SIGNUP, self.client, OK),
            (EDIT, self.client, FOUND),
            (DELETE, self.client, FOUND),
            (DETAIL, self.client, FOUND),
            (ADD, self.client, FOUND),
            (LIST, self.client, FOUND),
            (SUCCESS, self.client, FOUND),
            (EDIT, self.author_client, OK),
            (DELETE, self.author_client, OK),
            (DETAIL, self.author_client, OK),
            (ADD, self.auth_user_client, OK),
            (LIST, self.auth_user_client, OK),
            (SUCCESS, self.auth_user_client, OK),
            (EDIT, self.auth_user_client, NOT_FOUND),
            (DELETE, self.auth_user_client, NOT_FOUND),
            (DETAIL, self.auth_user_client, NOT_FOUND)
        )
        for url, user, expected_status in test_data:
            with self.subTest(url=url, user=user):
                self.assertEqual(user.get(url).status_code,
                                 expected_status)
                if url in (
                    EDIT, DELETE, DETAIL, ADD, LIST, SUCCESS
                ) and user == self.client:
                    self.assertRedirects(self.client.get(url),
                                         f'{REDIRECT}{url}')
