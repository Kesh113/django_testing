from .fixtures import TestBaseCase, ADD, LIST, EDIT
from notes.forms import NoteForm


class TestContextTemplates(TestBaseCase):
    def test_author_has_note_form(self):
        for url in (ADD, EDIT):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'), NoteForm)

    def test_note_in_list_author(self):
        response = self.author_client.get(LIST)
        self.assertIn(self.note, response.context['object_list'])
        note = response.context['object_list'].get(slug=self.note.slug)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)

    def test_note_not_in_list_auth_user(self):
        response = self.auth_user_client.get(LIST)
        self.assertNotIn(self.note, response.context['object_list'])
