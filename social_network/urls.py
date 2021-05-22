from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterApi


urlpatterns = [
    path('api/v1/posts/', include('posts.urls')),

    path('api/v1/users/', include('users.urls')),

    path('api/v1/analytics/', include('analytics.urls')),

    path('api/v1/auth/register/', RegisterApi.as_view()),
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
