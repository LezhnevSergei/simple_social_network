from typing import List

from rest_framework.exceptions import APIException

from posts.models import Post, PostLike


def create_post(creator_id: int, text: str) -> Post:
    post_data = {
        "text": text,
        "creator_id": creator_id,
    }

    post = Post.objects.create(**post_data)
    return post


def get_posts(posts: List[Post]) -> List[Post]:
    data = []
    for post in posts:
        post_data = {
            "id": post.id,
            "text": post.text,
            "created_at": post.created_at,
            "creator_id": post.creator.id,
            "count_likes": post.postlike_set.count(),
            "is_liked": post.is_liked(user_id=1)
        }
        data.append(post_data)

    return data


def get_post(post_id: int) -> Post:
    post_data = Post.objects.get(id=post_id)

    if post_data is None:
        raise APIException("The post doesn't exists")

    post = {
        "id": post_data.id,
        "text": post_data.text,
        "created_at": post_data.created_at,
        "creator_id": post_data.creator.id,
        "count_likes": post_data.postlike_set.count(),
        "is_liked": post_data.is_liked(user_id=1)
    }

    return post


def do_like(creator_id: int, post_id: int) -> PostLike:
    like_data = {
        "post_id": post_id,
        "creator_id": creator_id,
    }

    is_liked = Post.objects.get(id=like_data.get("post_id")).is_liked(user_id=like_data.get("creator_id"))
    if is_liked:
        raise APIException("This post has already been liked")

    like = PostLike.objects.create(**like_data)

    return like


def do_unlike(creator_id: int, post_id: int) -> None:
    like_data = {
        "post_id": post_id,
        "creator_id": creator_id,
    }

    is_liked = Post.objects.get(id=like_data.get("post_id")).is_liked(user_id=like_data.get("creator_id"))
    if not is_liked:
        raise APIException("This post has already been unliked")

    PostLike.objects.filter(**like_data).delete()
