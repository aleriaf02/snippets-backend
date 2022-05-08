from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model

from shared.models import VoteMixin
from topics.models import Topic

User = get_user_model()


class Snippet(VoteMixin, models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=25000, default='')
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='snippets',
        related_query_name='snippet'
    )
    topics = models.ManyToManyField(
        Topic, related_name='snippets')

    class Meta:
        ordering = ['-id']


class File(models.Model):
    name = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=25000, blank=False)
    snippet = models.ForeignKey(
        Snippet,
        on_delete=CASCADE,
        related_name='files',
        related_query_name='file'
    )

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments',
        related_query_name='comment'
    )
    snippet = models.ForeignKey(
        Snippet,
        on_delete=CASCADE,
        related_name='comments',
        related_query_name='comment'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=CASCADE
    )
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=25000, blank=False)

    class Meta:
        ordering = ['created_date']
