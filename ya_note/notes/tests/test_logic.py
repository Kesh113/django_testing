from http import HTTPStatus

from pytils.translit import slugify

from .fixtures import TestBaseCase, ADD, SUCCESS, DELETE, EDIT
from notes.forms import WARNING
from notes.models import Note


class TestNoteCreateEditDelete(TestBaseCase):
    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(ADD, data=self.form_data)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_user_can_create_note(self):
        notes = set(Note.objects.all())
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        created_note = notes.pop()
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.slug, self.form_data['slug'])
        self.assertEqual(created_note.author, self.auth_user)

    def test_not_unique_slug(self):
        notes = set(Note.objects.all())
        response = self.auth_user_client.post(ADD,
                                              data={'slug': self.note.slug})
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.note.slug + WARNING
        )
        self.assertEqual(set(Note.objects.all()), notes)

    def test_empty_slug(self):
        notes = set(Note.objects.all())
        self.form_data.pop('slug')
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        created_note = notes.pop()
        self.assertEqual(created_note.title, self.form_data['title'])
        self.assertEqual(created_note.text, self.form_data['text'])
        self.assertEqual(created_note.slug, slugify(self.form_data['title']))
        self.assertEqual(created_note.author, self.auth_user)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(DELETE)
        self.assertRedirects(response, SUCCESS)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edited_note.title, self.form_data['title'])
        self.assertEqual(edited_note.text, self.form_data['text'])
        self.assertEqual(edited_note.slug, self.form_data['slug'])
        self.assertEqual(edited_note.author, self.note.author)

    def test_user_cant_edit_other_note(self):
        notes = set(Note.objects.all())
        response = self.auth_user_client.post(EDIT, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.all()), notes)
        not_edited_note = Note.objects.get(id=self.note.id)
        self.assertEqual(not_edited_note.title, self.note.title)
        self.assertEqual(not_edited_note.text, self.note.text)
        self.assertEqual(not_edited_note.slug, self.note.slug)
        self.assertEqual(not_edited_note.author, self.note.author)

    def test_user_cant_delete_other_note(self):
        notes = set(Note.objects.all())
        response = self.auth_user_client.post(DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.all()), notes)
        not_deleted_note = Note.objects.get(id=self.note.id)
        self.assertEqual(not_deleted_note.title, self.note.title)
        self.assertEqual(not_deleted_note.text, self.note.text)
        self.assertEqual(not_deleted_note.slug, self.note.slug)
        self.assertEqual(not_deleted_note.author, self.note.author)
