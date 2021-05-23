from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from posts.models import Post
from posts.serializers import PostSerializer
from posts.services import get_posts, get_post, create_post


class PostsTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username='testuser1',
            password='password123',
        )
        self.client.force_login(self.user1)

        self.user2 = get_user_model().objects.create(
            username='testuser2',
            password='password123',
        )
        self.client.force_login(self.user2)

        self.post1 = Post.objects.create(text='Test post content 1', creator_id=self.user1.id)
        self.post2 = Post.objects.create(text='Test post content 2', creator_id=self.user2.id)

    def test_get_posts(self):
        posts = get_posts(current_user_id=self.user1.id)
        real_data = [
            {
                'id': self.post1.id,
                'text': 'Test post content 1',
                'created_at': self.post1.created_at,
                'creator_id': self.user1.id,
                'count_likes': 0,
                'is_liked': False
            },
            {
                'id': self.post2.id,
                'text': 'Test post content 2',
                'created_at': self.post2.created_at,
                'creator_id': self.user2.id,
                'count_likes': 0,
                'is_liked': False
            }
        ]

        self.assertEqual(real_data, posts)

    def test_get_post(self):
        post1 = get_post(post_id=self.post1.id, current_user_id=self.user1.id)
        real_post1 = {
            'id': self.post1.id,
            'text': 'Test post content 1',
            'created_at': self.post1.created_at,
            'creator_id': self.user1.id,
            'count_likes': 0,
            'is_liked': False
        }

        post2 = get_post(post_id=self.post2.id, current_user_id=self.user1.id)
        real_post2 = {
            'id': self.post2.id,
            'text': 'Test post content 2',
            'created_at': self.post2.created_at,
            'creator_id': self.user2.id,
            'count_likes': 0,
            'is_liked': False
        }

        self.assertEqual(real_post1, post1)
        self.assertEqual(real_post2, post2)

    def test_create_post(self):
        new_post_text = 'New post content'
        new_post = create_post(creator_id=self.user1.id, text=new_post_text)
        real_new_post = {
            'id': new_post.id,
            'text': new_post_text,
            'created_at': new_post.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'creator_id': self.user1.id,
            'count_likes': 0,
            'is_liked': False
        }

        serializer = PostSerializer(new_post)

        self.assertEqual(real_new_post, serializer.data)

