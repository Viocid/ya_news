from http import HTTPStatus

import pytest

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment
from news.pytest_tests.constant import COMMENT_FORM, COMMENT_BAD_WORDS

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, url_detail):
    st_comment_count = Comment.objects.count()
    client.post(url_detail, data=COMMENT_FORM)
    assert Comment.objects.count() == st_comment_count


def test_user_can_create_comment(author_client, url_detail, author, news):
    Comment.objects.all().delete()
    author_client.post(url_detail, data=COMMENT_FORM)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.author == author
    assert comment.text == COMMENT_FORM["text"]
    assert comment.news == news


def test_user_cant_use_bad_words(author_client, url_detail, comment):
    comments_count_s = Comment.objects.count()
    response = author_client.post(url_detail, data=COMMENT_BAD_WORDS)
    assertFormError(response, "form", "text", errors=WARNING)
    assert Comment.objects.count() == comments_count_s


def test_author_can_edit_comment(
    author_client, comment, url_edit, url_detail, news, author
):
    response = author_client.post(url_edit, COMMENT_FORM)
    assertRedirects(response, url_detail + "#comments")
    comment.refresh_from_db()
    assert comment.text == COMMENT_FORM["text"]
    assert comment.author == author
    assert comment.news == news


def test_other_user_cant_edit_comment(
    not_author_client, comment, url_edit, news, author
):
    response = not_author_client.post(url_edit, COMMENT_FORM)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news


def test_author_can_delete_comment(author_client, url_delete, url_detail):
    st_comment_count = Comment.objects.count() - 1
    response = author_client.post(url_delete)
    assertRedirects(response, url_detail + "#comments")
    assert Comment.objects.count() == st_comment_count


def test_other_user_cant_delete_comment(not_author_client, url_delete):
    st_comment_count = Comment.objects.count()
    response = not_author_client.post(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == st_comment_count
