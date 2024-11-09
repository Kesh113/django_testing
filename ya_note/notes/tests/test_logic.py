from http import HTTPStatus

from django.forms import model_to_dict
from pytils.translit import slugify

from .fixtures import TestBaseCase, ADD, SUCCESS, EDIT, DELETE
from notes.forms import WARNING
from notes.models import Note


class TestNoteCreateEditDelete(TestBaseCase):
    def test_anonymous_user_cant_create_note(self):
        self.client.post(ADD, data=self.form_data)
        self.assertEqual(list(Note.objects.values_list()), self.notes)

    def test_user_can_create_note(self):
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), self.notes_count + 1)
        self.assertTrue(
            Note.objects.filter(slug=self.form_data['slug']).exists())
        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.auth_user)

    def test_not_unique_slug(self):
        response = self.auth_user_client.post(ADD,
                                              data=model_to_dict(self.note))
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.note.slug + WARNING
        )
        self.assertEqual(list(Note.objects.values_list()), self.notes)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), self.notes_count + 1)
        new_slug = slugify(self.form_data['title'])
        self.assertTrue(
            Note.objects.filter(slug=new_slug).exists())
        new_note = Note.objects.get(slug=new_slug)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.auth_user)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(DELETE)
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), self.notes_count - 1)
        self.assertNotIn(self.note, Note.objects.all())

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        self.assertEqual(Note.objects.count(), self.notes_count)
        self.assertTrue(
            Note.objects.filter(slug=self.form_data['slug']).exists())
        new_note = Note.objects.get(slug=self.form_data['slug'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_user_cant_edit_delete_other_note(self):
        for url, data in ((EDIT, self.form_data), (DELETE, None)):
            with self.subTest(url=url):
                response = self.auth_user_client.post(url, data=data)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertEqual(list(Note.objects.values_list()), self.notes)
