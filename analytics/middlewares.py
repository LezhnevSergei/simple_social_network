from datetime import datetime

from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class AnalyticsUserRequestsMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if request.headers.get("Authorization"):
            token_row = request.headers.get("Authorization").split()[1]
            print(token_row)
            token = AccessToken(token_row)
            payload = token.payload
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            user.useranalytics_set.update(last_request_at=datetime.now())

        return response
