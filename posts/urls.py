from django.urls import path
from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, PostLikeViewSet


router = SimpleRouter()
router.register(f'', PostViewSet, 'posts')

urlpatterns = [
    path('like/', PostLikeViewSet.as_view({'post': 'create'}), name='like'),
]

urlpatterns += router.urls
