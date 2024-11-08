from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def auth_user_client(auth_user):
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def news(db):
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def news_with_different_dates(db):
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments_with_different_dates(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    return {
        'text': 'Текст нового комментария'
    }


@pytest.fixture
def urls_for_comment(comment_id_for_args, news_id_for_args):
    return {
        'edit': reverse('news:edit', args=comment_id_for_args),
        'delete': reverse('news:delete', args=comment_id_for_args),
        'success': reverse('news:detail', args=news_id_for_args) + '#comments'
    }


@pytest.fixture
def urls_for_news(news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    return {
        'detail': url,
        'success': url + '#comments'
    }
