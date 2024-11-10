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
        context_note = response.context['object_list'].get(id=self.note.id)
        self.assertEqual(self.note.title, context_note.title)
        self.assertEqual(self.note.text, context_note.text)
        self.assertEqual(self.note.slug, context_note.slug)
        self.assertEqual(self.note.author, context_note.author)

    def test_note_not_in_list_auth_user(self):
        self.assertNotIn(
            self.note, self.auth_user_client.get(LIST).context['object_list'])
