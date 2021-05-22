from django.urls import path

from posts.views import PostViewSet, PostLikeViewSet


urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='posts'),
    path('<int:post_id>/', PostViewSet.as_view({'get': 'retrieve'}), name='post'),
    path('like/', PostLikeViewSet.as_view({'post': 'create'}), name='like'),
]
