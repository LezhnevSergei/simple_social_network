from datetime import date, datetime

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from analytics.services import get_analytics_likes_on_period, get_analytics_likes_on_period_by_user
from posts.models import Post, PostLike


class AnalyticsLikesTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username='testuser',
            password='123123',
        )
        self.client.force_login(self.user1)

        self.user2 = get_user_model().objects.create(
            username='testuser2',
            password='123123',
        )
        self.client.force_login(self.user2)

        self.post1 = Post.objects.create(text='Test post content 1', creator_id=self.user1.id)
        self.post2 = Post.objects.create(text='Test post content 1', creator_id=self.user2.id)

        self.like1 = PostLike.objects.create(creator_id=self.user1.id, post_id=self.post1.id)
        self.like2 = PostLike.objects.create(creator_id=self.user1.id, post_id=self.post2.id)
        self.like3 = PostLike.objects.create(creator_id=self.user2.id, post_id=self.post1.id)

    def test_get_analytics_likes_on_period(self):
        analytics = get_analytics_likes_on_period(gte='2000-01-01', lte='2099-01-01')
        real_analytics = {
            datetime.now().date().strftime('%Y-%m-%d'): 3
        }

        self.assertEqual(real_analytics, analytics)

    def test_get_analytics_likes_on_period_by_user(self):
        analytics = get_analytics_likes_on_period_by_user(user_id=self.user1.id, gte='2000-01-01', lte='2099-01-01')
        real_analytics = {
            datetime.now().date().strftime('%Y-%m-%d'): 2
        }

        self.assertEqual(real_analytics, analytics)
