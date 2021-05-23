from django.urls import path

from analytics.views import AnalyticsLikesViewSet, AnalyticsUserViewSet

urlpatterns = [
    path('', AnalyticsLikesViewSet.as_view({'get': 'retriev'})),
    path('users/', AnalyticsUserViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/', AnalyticsUserViewSet.as_view({'get': 'retriev'})),
]
