from django.urls import path, include
from rest_framework import routers

from posts.views import PostViewSet, PostLikeViewSet


posts = routers.DefaultRouter()
posts.register(r'', PostViewSet, basename='posts')
posts.register(r'like', PostLikeViewSet, basename='like')


urlpatterns = [
    path('', include(posts.urls)),
]
