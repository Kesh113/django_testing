from django.conf import settings

from news.forms import CommentForm


def test_auth_user_has_comment_form(auth_user_client, detail):
    assert isinstance(auth_user_client.get(detail).context.get('form'),
                      CommentForm)


def test_not_auth_user_has_not_comment_form(client, detail):
    assert 'form' not in client.get(detail).context


def test_comments_order(client, comments_with_different_dates, detail):
    response = client.get(detail)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_news_order(client, news_with_different_dates, home):
    all_dates = [news.date for news in client.get(home).context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_news_count(client, news_with_different_dates, home):
    assert (
        client.get(home).context['object_list'].count()
    ) == settings.NEWS_COUNT_ON_HOME_PAGE
