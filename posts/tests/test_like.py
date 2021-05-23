from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from posts.models import Post, PostLike
from posts.services import do_like, do_unlike


class PostLikeTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username='testuser',
            password='123123',
        )
        self.client.force_login(self.user1)

        self.post = Post.objects.create(text='Test post content 1', creator_id=self.user1.id)

    def test_do_like(self):
        like = do_like(post_id=self.post.id, creator_id=self.user1.id)

        like_data = {
            'id': like.id,
            'creator_id': like.creator_id,
            'post_id': like.post_id,
            'created_at': like.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }

        real_like = {
            'id': like.id,
            'created_at': like.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'creator_id': self.user1.id,
            'post_id': self.post.id,
        }

        self.assertEqual(real_like, like_data)

    def test_do_unlike(self):
        like = do_like(post_id=self.post.id, creator_id=self.user1.id)
        do_unlike(post_id=self.post.id, creator_id=self.user1.id)
        like = PostLike.objects.filter(id=like.id).first()

        self.assertIsNone(like)
