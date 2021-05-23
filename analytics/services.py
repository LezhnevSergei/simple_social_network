from datetime import date, datetime
from typing import Dict, List

from django.contrib.auth.models import User

from posts.models import PostLike


def get_analytics_likes_on_period(gte: str, lte: str) -> Dict[str, int]:
    likes = PostLike.objects.filter(created_at__gte=gte, created_at__lte=lte)
    analytics_likes_by_date = _count_likes_by_created_at(likes)

    return analytics_likes_by_date


def get_analytics_likes_on_period_by_user(user_id: int, gte: str, lte: str) -> Dict[str, int]:
    likes = PostLike.objects.filter(creator_id=user_id, created_at__gte=gte, created_at__lte=lte)
    analytics_likes_by_date = _count_likes_by_created_at(likes)

    return analytics_likes_by_date


def get_user_analytics(user_id: int) -> Dict[str, datetime]:
    user = User.objects.get(id=user_id)
    result = _get_user_analytics_value(user)

    return result


def get_users_analytics() -> List[Dict[str, datetime]]:
    users = User.objects.all()

    result = []
    for user in users:
        result.append(_get_user_analytics_value(user))

    return result


def _get_user_analytics_value(user: User):
    last_login = user.last_login
    last_request_at = user.useranalytics_set.get(user_id=user.id).last_request_at

    result = {
        "user_id": user.id,
        "last_login_at": last_login,
        "last_request_at": last_request_at
    }

    return result


def _count_likes_by_created_at(likes: List[PostLike]) -> Dict[str, int]:
    analytics_likes_by_date = {}
    for like in likes:
        day = str(like.created_at.date())
        if analytics_likes_by_date.get(day):
            analytics_likes_by_date[day] += 1
        else:
            analytics_likes_by_date[day] = 1

    return analytics_likes_by_date
