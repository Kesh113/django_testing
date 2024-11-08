from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )
        cls.edit = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete = reverse('notes:delete', args=(cls.note.slug,))
        cls.detail = reverse('notes:detail', args=(cls.note.slug,))
        cls.add = reverse('notes:add')
        cls.list = reverse('notes:list')
        cls.success = reverse('notes:success')

    def test_pages_availability(self):
        urls = (
            reverse('notes:home'),
            reverse('users:login'),
            reverse('users:logout'),
            reverse('users:signup'),
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code,
                                 HTTPStatus.OK)

    def test_availability_for_note_read_edit_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in (self.edit, self.delete, self.detail):
                with self.subTest(user=user, url=url):
                    self.assertEqual(self.client.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.edit,
            self.delete,
            self.detail,
            self.add,
            self.list,
            self.success
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{reverse("users:login")}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)

    def test_pages_availability_for_auth_client(self):
        self.client.force_login(self.reader)
        for url in (self.add, self.list, self.success):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code,
                                 HTTPStatus.OK)
