import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, all_news, url_home):
    response = client.get(url_home)
    news_count = response.context["object_list"].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news, url_home):
    response = client.get(url_home)
    news_on_page = response.context["object_list"]
    all_dates = [news.date for news in news_on_page]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, all_comments, news, url_detail):
    response = client.get(url_detail)
    assert "news" in response.context
    all_timestamps = [comment.created for comment in news.comment_set.all()]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_comment_contains_form(author_client, url_detail):
    response = author_client.get(url_detail)
    assert "form" in response.context
    assert isinstance(response.context["form"], CommentForm)


def test_anonymous_client_has_no_form(client, url_detail):
    response = client.get(url_detail)
    assert "form" not in response.context
