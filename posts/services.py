from typing import List, Optional

from rest_framework.exceptions import APIException

from posts.models import Post, PostLike


def create_post(creator_id: int, text: str) -> Post:
    post_data = {
        "text": text,
        "creator_id": creator_id,
    }
    new_post = Post.objects.create(**post_data)

    return new_post


def get_posts(current_user_id: int, user_id: Optional[int] = None) -> List[Post]:
    data = []
    if user_id:
        posts = Post.objects.filter(creator_id=user_id)
    else:
        posts = Post.objects.all()

    for post in posts:
        post_data = {
            "id": post.id,
            "text": post.text,
            "created_at": post.created_at,
            "creator_id": post.creator.id,
            "count_likes": post.postlike_set.count(),
            "is_liked": post.get_is_liked(user_id=current_user_id)
        }
        data.append(post_data)

    return data


def get_post(post_id: int, current_user_id: int) -> dict:
    try:
        post_data = Post.objects.get(id=post_id)
    except Exception:
        raise APIException("Post not exists")

    post = {
        "id": post_data.id,
        "text": post_data.text,
        "created_at": post_data.created_at,
        "creator_id": post_data.creator.id,
        "count_likes": post_data.postlike_set.count(),
        "is_liked": post_data.get_is_liked(user_id=current_user_id)
    }

    return post


def delete_post(post_id: int, user_id: int) -> None:
    try:
        post = Post.objects.get(id=post_id)
    except Exception:
        raise APIException("Post not exists")

    if post.creator_id != user_id:
        raise APIException("User cannot delete other user's posts")

    post.delete()


def do_like(creator_id: int, post_id: int) -> PostLike:
    like_data = {
        "post_id": post_id,
        "creator_id": creator_id,
    }

    is_liked = Post.objects.get(id=like_data.get("post_id")).get_is_liked(user_id=like_data.get("creator_id"))
    if is_liked:
        raise APIException("This post has already been liked")

    like = PostLike.objects.create(**like_data)

    return like


def do_unlike(creator_id: int, post_id: int) -> None:
    like_data = {
        "post_id": post_id,
        "creator_id": creator_id,
    }

    is_liked = Post.objects.get(id=like_data.get("post_id")).get_is_liked(user_id=like_data.get("creator_id"))
    if not is_liked:
        raise APIException("This post has already been unliked")

    PostLike.objects.filter(**like_data).delete()
