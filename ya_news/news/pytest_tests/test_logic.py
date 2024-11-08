from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(client, form_data, urls_for_news):
    client.post(urls_for_news['detail'], data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(auth_user, auth_user_client, news,
                                 urls_for_news, form_data):
    response = auth_user_client.post(urls_for_news['detail'], data=form_data)
    assertRedirects(response, urls_for_news['success'])
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == auth_user


def test_user_cant_use_bad_words(auth_user_client, urls_for_news):
    response = auth_user_client.post(
        urls_for_news['detail'],
        data={'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    )
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, urls_for_comment):
    assertRedirects(author_client.delete(urls_for_comment['delete']),
                    urls_for_comment['success'])
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(auth_user_client,
                                                  urls_for_comment):
    assert auth_user_client.delete(
        urls_for_comment['delete']
    ).status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, comment, form_data,
                                 urls_for_comment):
    assertRedirects(author_client.post(
        urls_for_comment['edit'], data=form_data), urls_for_comment['success'])
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(auth_user_client, form_data,
                                                comment, urls_for_comment):
    text = comment.text
    assert auth_user_client.post(
        urls_for_comment['edit'], data=form_data
    ).status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == text
