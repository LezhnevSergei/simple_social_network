from rest_framework import viewsets
from rest_framework.response import Response

from analytics.services import get_analytics_likes_on_period, get_analytics_likes_on_period_by_user, get_user_analytics, \
    get_users_analytics


class AnalyticsLikesViewSet(viewsets.ViewSet):
    def retriev(self, request, *args, **kwargs):
        gte = request.query_params.get('date_from')
        lte = request.query_params.get('date_to')
        user_id = request.query_params.get('user_id')

        if user_id:
            analytics_likes_by_date = get_analytics_likes_on_period_by_user(user_id=user_id, gte=gte, lte=lte)
        else:
            analytics_likes_by_date = get_analytics_likes_on_period(gte=gte, lte=lte)

        return Response(analytics_likes_by_date)


class AnalyticsUserViewSet(viewsets.ViewSet):
    def retriev(self, request, user_id: int, *args, **kwargs):
        response = get_user_analytics(user_id)

        return Response(response)

    def list(self, request):
        response = get_users_analytics()

        return Response(response)
