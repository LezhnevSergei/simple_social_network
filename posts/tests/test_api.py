from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, PostLike
from posts.serializers import PostSerializer


class PostsTestCase(APITestCase):
    def setUp(self):
        self.api_base = '/api/v1/'

        url_register = self.api_base + 'auth/register/'
        user_data = {'username': 'testuser', 'password': 'password123'}
        register_response = self.client.post(url_register, user_data, format='json')
        url_login = self.api_base + 'auth/login/'
        login_response = self.client.post(url_login, user_data, format='json')

        self.user = {
            'id': register_response.json().get('user').get('id'),
            'username': user_data.get('username'),
            'password': user_data.get('password'),
            'access': login_response.json().get('access'),
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.get('access'))

        post = Post.objects.create(text='Test post content 1', creator_id=self.user.get('id'))
        self.post = PostSerializer(post).data

    def test_register(self):
        url = self.api_base + 'auth/register/'
        user_data = {'username': 'testuser2', 'password': 'password123'}

        count_users_before_registration = get_user_model().objects.count()
        response = self.client.post(url, user_data, format='json')
        count_users = get_user_model().objects.count()

        self.assertEqual(count_users_before_registration + 1, count_users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        url_login = self.api_base + 'auth/login/'
        user_data = {
            'username': self.user.get('username'),
            'password': self.user.get('password'),
        }

        response = self.client.post(url_login, user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_posts(self):
        url = reverse('posts-list')
        response = self.client.get(url)

        posts = response.json()

        self.assertEqual(posts, [self.post])

    def test_get_post(self):
        url = reverse('posts-detail', args=[self.post.get('id')])
        response = self.client.get(url)

        posts = response.json()

        self.assertEqual(posts, self.post)

    def test_like_post(self):
        url = reverse('like') + '?do_act=like'

        like_data = {
            'post_id': self.post.get('id'),
        }

        response = self.client.post(url, like_data, format='json')

        real_data = {'creator_id': self.user.get('id'), 'is_liked': True}

        self.assertEqual(real_data, response.json())

    def test_unlike_post(self):
        do_like_url = reverse('like') + '?do_act=like'
        do_unlike_url = reverse('like') + '?do_act=unlike'
        like_data = {
            'post_id': self.post.get('id'),
        }
        do_like_response = self.client.post(do_like_url, like_data, format='json')
        response = self.client.post(do_unlike_url, like_data, format='json')

        real_data = {'creator_id': self.user.get('id'), 'is_liked': False}

        like = PostLike.objects.filter(post_id=self.post.get('id'), creator_id=do_like_response.get('creator_id')).first()

        self.assertEqual(real_data, response.json())
        self.assertIsNone(like)

    def test_is_liked(self):
        do_like_url = reverse('like') + '?do_act=like'

        like_data = {
            'post_id': self.post.get('id'),
        }

        self.client.post(do_like_url, like_data, format='json')

        get_post_url = reverse('posts-detail', args=[self.post.get('id')])
        post_response = self.client.get(get_post_url)
        is_liked = post_response.json().get('is_liked')

        self.assertTrue(is_liked)

    def test_count_like(self):
        do_like_url = reverse('like') + '?do_act=like'

        like_data = {
            'post_id': self.post.get('id'),
        }

        self.client.post(do_like_url, like_data, format='json')

        get_post_url = reverse('posts-detail', args=[self.post.get('id')])
        post_response = self.client.get(get_post_url)
        count_likes = post_response.json().get('count_likes')
        real_count_likes = PostLike.objects.count()

        self.assertEqual(real_count_likes, count_likes)
