import json
import random

import requests


def users_register_login_create_posts(count_users, max_count_posts):
    users_state = {}

    for user_index in range(count_users):
        random_number = random.random()
        user_data = {'username': f'User{random_number}', 'password': f'password{random_number}'}
        registered_data = _user_register(**user_data)
        user_data_with_id = {**user_data, 'id': registered_data.get('user').get('id')}
        access_data = _user_login(**user_data)
        access_token = access_data.get('access')

        users_state[user_data_with_id.get('id')] = {**user_data, 'access_token': access_token}

        count_posts = random.randint(1, max_count_posts)

        for post_index in range(count_posts):
            _create_post(f"Post content by {user_data.get('username')}", access_token)

    return users_state


def users_do_likes(users_state, max_count_likes):
    for user_id, user_data in users_state.items():
        user_access_token = user_data.get('access_token')
        posts = _get_posts(user_access_token)
        count_likes = random.randint(1, max_count_likes)
        i = 0
        while True:
            do_like = random.randint(0, 1) % 2 == 0

            post = posts[i]
            if not post.get('is_liked') and do_like:
                _like_post(post_id=post.get('id'), access_token=user_access_token)
                posts[i]['is_liked'] = True
                count_likes -= 1

                if count_likes == 0:
                    break

            i += 1
            if i == len(posts):
                i = 0


def _user_register(username: str, password: str) -> dict:
    new_user_data = {'username': username, 'password': password}
    headers = {'Content-type': 'application/json'}
    response = requests.post(
        'http://localhost:1337/api/v1/auth/register/',
        json.dumps(new_user_data),
        headers=headers
    )

    return response.json()


def _user_login(username: str, password: str) -> dict:
    user_data = {'username': username, 'password': password}
    headers = {'Content-type': 'application/json'}
    response = requests.post(
        'http://localhost:1337/api/v1/auth/login/',
        json.dumps(user_data),
        headers=headers
    )

    return response.json()


def _get_posts(access_token: str) -> dict:
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    response = requests.get(
        f'http://localhost:1337/api/v1/posts/',
        headers=headers
    )

    return response.json()


def _create_post(post_content: str, access_token: str) -> dict:
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    post = {'text': post_content}
    response = requests.post(
        f'http://localhost:1337/api/v1/posts/',
        json=post,
        headers=headers
    )

    return response.json()


def _get_post(post_id: int, access_token: str) -> dict:
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    response = requests.get(
        f'http://localhost:1337/api/v1/posts/{post_id}',
        headers=headers
    )

    return response.json()


def _like_post(post_id: int, access_token: str) -> dict:
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    response = requests.post(
        f'http://localhost:1337/api/v1/posts/like/?do_act=like',
        json={'post_id': post_id},
        headers=headers
    )

    return response.json()


def _unlike_post(post_id: int, access_token: str) -> dict:
    headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + access_token}
    response = requests.post(
        f'http://localhost:1337/api/v1/posts/like/?do_act=unlike',
        json={'post_id': post_id},
        headers=headers
    )

    return response.json()
