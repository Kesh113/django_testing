from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()

NOTE_SLUG = 'slug'

ADD = reverse('notes:add')
LIST = reverse('notes:list')
SUCCESS = reverse('notes:success')
HOME = reverse('notes:home')
LOGIN = reverse('users:login')
LOGOUT = reverse('users:logout')
SIGNUP = reverse('users:signup')
DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
EDIT = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE = reverse('notes:delete', args=(NOTE_SLUG,))


class TestBaseCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="Лев Толстой")
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.auth_user = User.objects.create(username="Не Лев Толстой")
        cls.auth_user_client = Client()
        cls.auth_user_client.force_login(cls.auth_user)

        cls.note = Note.objects.create(
            title="Заголовок", text="Текст заметки",
            slug=NOTE_SLUG, author=cls.author
        )

        cls.form_data = {'title': 'Новый заголовок',
                         'text': 'Новый текст заметки',
                         'slug': 'noviy-slug'}

        cls.notes = list(Note.objects.values_list())

        cls.notes_count = Note.objects.count()
