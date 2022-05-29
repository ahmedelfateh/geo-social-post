from django.db import models
from app.users.models import User
from django.contrib.postgres.fields import ArrayField


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name="posts"
    )
    body = models.TextField()
    like = ArrayField(
        models.IntegerField(blank=True),
        default=list,
    )
    unlike = ArrayField(
        models.IntegerField(blank=True),
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["user", "created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    @property
    def like_count(self):
        return len(self.like)

    @property
    def unlike_count(self):
        return len(self.unlike)
