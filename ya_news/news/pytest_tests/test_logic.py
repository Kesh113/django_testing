from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


FORM_DATA = {'text': 'Текст нового комментария'}
WRONG_DATA = (
    {'text': f'Какой-то текст, {bad}, еще текст'} for bad in BAD_WORDS)


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


@pytest.mark.parametrize('wrong_form_field', WRONG_DATA)
def test_user_cant_use_wrong_data(auth_user_client, wrong_form_field, detail):
    response = auth_user_client.post(
        detail,
        data=wrong_form_field
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete, success):
    assertRedirects(author_client.delete(delete), success)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(auth_user_client, comment,
                                                  delete):
    assert auth_user_client.delete(delete).status_code == HTTPStatus.NOT_FOUND
    assert comment in Comment.objects.all()
    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.news == comment.news
    assert edited_comment.author == comment.author
    assert edited_comment.text == comment.text


def test_author_can_edit_comment(author_client, edit, comment, success):
    assertRedirects(author_client.post(edit, data=FORM_DATA), success)
    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.news == comment.news
    assert edited_comment.author == comment.author
    assert edited_comment.text == FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(auth_user_client, edit,
                                                comment):
    assert auth_user_client.post(
        edit, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND
    edited_comment = Comment.objects.get(id=comment.id)
    assert edited_comment.news == comment.news
    assert edited_comment.author == comment.author
    assert edited_comment.text == comment.text
