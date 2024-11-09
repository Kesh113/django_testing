from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from .conftest import TEXT
from news.forms import BAD_WORDS, WARNING
from news.models import Comment


BAD_TEXT = 'Какой-то текст, еще текст, '
FORM_DATA = {'text': 'Текст нового комментария'}


def test_anonymous_user_cant_create_comment(client, detail):
    client.post(detail, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(auth_user, auth_user_client, news,
                                 detail, success):
    response = auth_user_client.post(detail, data=FORM_DATA)
    assertRedirects(response, success)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == auth_user


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(auth_user_client, bad_word, detail):
    response = auth_user_client.post(
        detail,
        data={'text': BAD_TEXT + bad_word}
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete, success):
    assertRedirects(author_client.delete(delete), success)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(auth_user_client, comment,
                                                  delete):
    old_count = Comment.objects.count()
    assert auth_user_client.delete(delete).status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == old_count
    new_comment = Comment.objects.get()
    assert new_comment.text == comment.text
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author


def test_author_can_edit_comment(author, news, author_client, comment,
                                 edit, success):
    assertRedirects(author_client.post(edit, data=FORM_DATA), success)
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(author, news, comment,
                                                auth_user_client, edit):
    assert auth_user_client.post(
        edit, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get()
    assert comment.text == TEXT
    assert comment.news == news
    assert comment.author == author
