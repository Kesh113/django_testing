from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestContextTemplates(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.not_author = User.objects.create(username='Не Лев Толстой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_author_has_note_form(self):
        self.client.force_login(self.author)
        for name, slug in (('notes:add', None), ('notes:edit',
                                                 (self.note.slug,))):
            with self.subTest(name=name):
                response = self.client.get(reverse(name, args=slug))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_list_for_different_users(self):
        for user, has_note in ((self.not_author, False),
                               (self.author, True)):
            self.client.force_login(user)
            with self.subTest(name=user.username):
                response = self.client.get(reverse('notes:list'))
                self.assertIs(self.note in response.context['object_list'],
                              has_note)
