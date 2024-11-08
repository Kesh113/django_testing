import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.parametrize(
    'parametrized_client, has_form',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('auth_user_client'), True),
    )
)
def test_page_detail_has_comment_form(parametrized_client, has_form,
                                      urls_for_news):
    response = parametrized_client.get(urls_for_news['detail'])
    assert ('form' in response.context) is has_form
    if has_form:
        assert isinstance(response.context['form'], CommentForm)


def test_comments_order(client, comments_with_different_dates, urls_for_news):
    response = client.get(urls_for_news['detail'])
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_news_order(client, news_with_different_dates):
    response = client.get(reverse('news:home'))
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_news_count(client, news_with_different_dates):
    news_count = client.get(
        reverse('news:home')
    ).context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
