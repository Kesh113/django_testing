from http import HTTPStatus

from .fixtures import (TestBaseCase, ADD, DETAIL, LIST, SUCCESS, EDIT, DELETE,
                       HOME, LOGIN, LOGOUT, SIGNUP, REDIRECT_EDIT,
                       REDIRECT_DELETE, REDIRECT_DETAIL, REDIRECT_ADD,
                       REDIRECT_LIST, REDIRECT_SUCCESS)


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
        test_data = (
            (EDIT, REDIRECT_EDIT),
            (DELETE, REDIRECT_DELETE),
            (DETAIL, REDIRECT_DETAIL),
            (ADD, REDIRECT_ADD),
            (LIST, REDIRECT_LIST),
            (SUCCESS, REDIRECT_SUCCESS)
        )
        for url, url_redirect in test_data:
            with self.subTest(url=url, url_redirect=url_redirect):
                self.assertRedirects(self.client.get(url), url_redirect)
