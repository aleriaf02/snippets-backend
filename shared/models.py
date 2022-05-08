from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F


class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="votes",
    )
    score = models.IntegerField(default=1)

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return "{}:{}:{}".format(self.user, self.content_object, self.score)

    @classmethod
    def vote_with_user_object(cls, content_object, user_object, score):
        return Vote(content_object=content_object, user=user_object, score=score)


class VoteMixin(models.Model):
    votes = GenericRelation(Vote)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        abstract = True

    @property
    def total_score(self):
        return self.upvotes + self.downvotes

    def _get_with_object(self, user_object):
        return self.votes.get(user=user_object)

    def _update_score(self, diff_up, diff_down):
        self.upvotes += diff_up
        self.downvotes += diff_down

        self.__class__.objects.filter(id=self.id).update(
            upvotes=F("upvotes") + diff_up,
            downvotes=F("downvotes") + diff_down,
        )

    def upvote(self, user_object):
        """Upvote the instance with provided user."""

        diff_down = 0

        try:
            # Already voted content
            vote = self._get_with_object(user_object)
            if vote.score == 1:
                # Cancel previous upvote
                vote.delete()
                # Remove 1 upvote
                diff_up = -1
            else:
                # Previously downvoted
                vote.score = 1
                vote.save()
                # Remove downvote and add upvote
                diff_down = 1
                diff_up = 1

        except Vote.DoesNotExist:
            vote = Vote.vote_with_user_object(
                content_object=self, user_object=user_object, score=1
            )
            vote.save()
            diff_up = 1

        self._update_score(diff_up, diff_down)

    def downvote(self, user_object):
        """Downvote the instance with the provided user."""

        diff_up = 0

        try:
            # Already voted content
            vote = self._get_with_object(user_object)
            if vote.score == -1:
                # Cancel previous downvote
                vote.delete()
                # Remove 1 downvote
                diff_down = 1
            else:
                # Previously upvoted
                vote.score = -1
                vote.save()
                # Remove upvote and add downvote
                diff_up = -1
                diff_down = -1

        except Vote.DoesNotExist:
            vote = Vote.vote_with_user_object(
                content_object=self, user_object=user_object, score=-1
            )
            vote.save()
            diff_down = -1

        self._update_score(diff_up, diff_down)
