import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (("news:home", None),),
)
def test_news_count(client, all_news, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    object_list = response.context["object_list"]
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (("news:home", None),),
)
def test_news_order(client, all_news, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    object_list = response.context["object_list"]
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (("news:detail", pytest.lazy_fixture("id_for_args")),),
)
def test_comments_order(client, all_comments, name, args, news):
    url = reverse(name, args=args)
    response = client.get(url)
    assert "news" in response.context
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (("news:detail", pytest.lazy_fixture("id_for_args")),),
)
def test_comment_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert "form" in response.context


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, args",
    (("news:detail", pytest.lazy_fixture("id_for_args")),),
)
def test_anonymous_client_has_no_form(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert "form" not in response.context
