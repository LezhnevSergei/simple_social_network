from django.urls import path

from users.views import UserPostsViewSet

urlpatterns = [
      path('<int:user_id>/posts/', UserPostsViewSet.as_view({'get': 'list'})),
]
