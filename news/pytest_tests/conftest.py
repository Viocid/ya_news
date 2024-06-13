from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username="Автор")


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username="Не автор")


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(title="title", text="text")


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text="text comment",
    )


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f"Новость {index}",
            text="Просто текст.",
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def all_comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f"Tекст {index}",
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def url_home():
    return reverse("news:home")


@pytest.fixture
def url_detail(news):
    return reverse("news:detail", args=(news.id,))


@pytest.fixture
def url_edit(comment):
    return reverse("news:edit", args=(comment.id,))


@pytest.fixture
def url_delete(comment):
    return reverse("news:delete", args=(comment.id,))


@pytest.fixture
def url_reverse(url_delete, url_edit, news):
    return (
        url_home,
        reverse("users:login"),
        reverse("users:logout"),
        reverse("users:signup"),
        url_detail,
    )


@pytest.fixture
def url_login():
    return reverse("users:login")


@pytest.fixture
def url_logout():
    return reverse("users:logout")


@pytest.fixture
def url_signup():
    return reverse("users:signup")


@pytest.fixture
def param_client():
    return (
        (pytest.lazy_fixture("not_author_client")),
        (pytest.lazy_fixture("author_client")),
    )


@pytest.fixture
def expected_status():
    return (
        (HTTPStatus.NOT_FOUND),
        (HTTPStatus.OK),
    )
