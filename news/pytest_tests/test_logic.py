from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, comment_form, id_for_args):
    url = reverse("news:detail", args=id_for_args)
    client.post(url, data=comment_form)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(author_client, comment_form, id_for_args):
    url = reverse("news:detail", args=id_for_args)
    author_client.post(url, data=comment_form)
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_user_cant_use_bad_words(
    author_client, comment_form, id_for_args, comment
):
    url = reverse("news:detail", args=id_for_args)
    comment_form["text"] = f"Какой-то текст, {BAD_WORDS[0]}, еще текст"
    response = author_client.post(url, data=comment_form)
    assertFormError(response, "form", "text", errors=WARNING)
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_author_can_edit_comment(
    id_for_args, author_client, comment_form, comment, id_comment_for_args
):
    url = reverse("news:edit", args=id_comment_for_args)
    response = author_client.post(url, comment_form)
    assertRedirects(
        response, reverse("news:detail", args=id_for_args) + "#comments"
    )
    comment.refresh_from_db()
    assert comment.text == comment_form["text"]


def test_other_user_cant_edit_comment(
    not_author_client, comment_form, comment, id_comment_for_args
):
    url = reverse("news:edit", args=id_comment_for_args)
    response = not_author_client.post(url, comment_form)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=id_comment_for_args[0])
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
    author_client, id_comment_for_args, id_for_args
):
    url = reverse("news:delete", args=id_comment_for_args)
    response = author_client.post(url)
    assertRedirects(
        response, reverse("news:detail", args=id_for_args) + "#comments"
    )
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(
    not_author_client, id_comment_for_args
):
    url = reverse("news:delete", args=id_comment_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
