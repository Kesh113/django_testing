from http import HTTPStatus

from pytils.translit import slugify

from .fixtures import TestBaseCase, ADD, SUCCESS, DELETE, EDIT
from notes.forms import WARNING
from notes.models import Note


# NOTES = set(Note.objects.values_list())


class TestNoteCreateEditDelete(TestBaseCase):
    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.values_list())
        self.client.post(ADD, data=self.form_data)
        self.assertEqual(set(Note.objects.values_list()), notes)

    def test_user_can_create_note(self):
        notes = set(Note.objects.values_list())
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        created_note = set(Note.objects.values_list()).difference(notes)
        self.assertEqual(len(created_note), 1)
        created_note = next(iter(created_note))
        self.assertEqual(created_note[1], self.form_data['title'])
        self.assertEqual(created_note[2], self.form_data['text'])
        self.assertEqual(created_note[3], self.form_data['slug'])
        self.assertEqual(created_note[4], self.auth_user.id)

    def test_not_unique_slug(self):
        notes = set(Note.objects.values_list())
        response = self.auth_user_client.post(ADD,
                                              data={'slug': self.note.slug})
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.note.slug + WARNING
        )
        self.assertEqual(set(Note.objects.values_list()), notes)

    def test_empty_slug(self):
        notes = set(Note.objects.values_list())
        self.form_data.pop('slug')
        response = self.auth_user_client.post(ADD, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        created_note = set(Note.objects.values_list()).difference(notes)
        self.assertEqual(len(created_note), 1)
        created_note = next(iter(created_note))
        self.assertEqual(created_note[1], self.form_data['title'])
        self.assertEqual(created_note[2], self.form_data['text'])
        self.assertEqual(created_note[3], slugify(self.form_data['title']))
        self.assertEqual(created_note[4], self.auth_user.id)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(DELETE)
        self.assertRedirects(response, SUCCESS)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_author_can_edit_note(self):
        notes = set(Note.objects.values_list())
        response = self.author_client.post(EDIT, data=self.form_data)
        self.assertRedirects(response, SUCCESS)
        edited_note = set(Note.objects.values_list()).difference(notes)
        self.assertEqual(len(edited_note), 1)
        old_fields = list(self.form_data.values()) + [self.note.author.id]
        for new_field, old_field in zip(next(iter(edited_note))[1:5],
                                        old_fields):
            self.assertEqual(new_field, old_field)

    def test_user_cant_edit_other_note(self):
        notes = set(Note.objects.values_list())
        response = self.auth_user_client.post(EDIT, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.values_list()), notes)

    def test_user_cant_delete_other_note(self):
        notes = set(Note.objects.values_list())
        response = self.auth_user_client.post(DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.values_list()), notes)
