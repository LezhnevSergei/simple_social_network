from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response

from analytics.models import UserAnalytics
from posts.serializers import PostSerializer
from posts.services import get_posts
from .serializers import RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserAnalytics.objects.create(user_id=user.id)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserPostsViewSet(viewsets.ViewSet):
    def list(self, request, user_id: int):
        posts = get_posts(current_user_id=request.user.id, user_id=user_id)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
