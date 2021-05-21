from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    text = models.TextField()
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_is_liked(self, user_id: int) -> bool:
        is_liked = self.postlike_set.values().filter(post_id=self.id, creator_id=user_id).first() is not None
        return is_liked


class PostLike(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
