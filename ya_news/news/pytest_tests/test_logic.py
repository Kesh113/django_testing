from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


FORM_DATA = {'text': 'Текст нового комментария'}


def test_anonymous_user_cant_create_comment(client, detail):
    comments = set(Comment.objects.values_list())
    client.post(detail, data=FORM_DATA)
    assert set(Comment.objects.values_list()) == comments


def test_user_can_create_comment(auth_user, auth_user_client, news,
                                 detail, success):
    response = auth_user_client.post(detail, data=FORM_DATA)
    assertRedirects(response, success)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == auth_user


@pytest.mark.parametrize('bad_text', (
    {'text': f'Какой-то текст, {bad}, еще текст'} for bad in BAD_WORDS))
def test_user_cant_use_bad_words(auth_user_client, bad_text, detail):
    response = auth_user_client.post(
        detail,
        data=bad_text
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete, success):
    assertRedirects(author_client.delete(delete), success)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(auth_user_client, delete):
    comments = set(Comment.objects.values_list())
    assert auth_user_client.delete(delete).status_code == HTTPStatus.NOT_FOUND
    assert set(Comment.objects.values_list()) == comments


def test_author_can_edit_comment(author_client, edit, comment, success):
    comments = set(Comment.objects.values_list())
    assertRedirects(author_client.post(edit, data=FORM_DATA), success)
    edited_comment = set(Comment.objects.values_list()).difference(comments)
    assert len(edited_comment) == 1
    edited_comment = next(iter(edited_comment))
    assert edited_comment[1] == comment.news.id
    assert edited_comment[2] == comment.author.id
    assert edited_comment[3] == FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(auth_user_client, edit):
    comments = set(Comment.objects.values_list())
    assert auth_user_client.post(
        edit, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    assert set(Comment.objects.values_list()) == comments
