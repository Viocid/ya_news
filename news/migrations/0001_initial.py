# Generated by Django 3.2.15 on 2022-10-25 13:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("text", models.TextField()),
                ("date", models.DateField()),
            ],
            options={
                "ordering": ("-date",),
                "verbose_name": "Новость",
                "verbose_name_plural": "Новости",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "news",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.news",
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
            },
        ),
    ]
