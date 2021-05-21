from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer, PostLikeSerializer
from posts.services import create_post, get_posts, get_post, do_like, do_unlike


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()

    def retrieve(self, request, pk: int):
        post = get_post(pk)
        serializer = PostSerializer(post)

        return Response(serializer.data)

    def list(self, request):
        posts = get_posts(self.queryset)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def create(self, request):
        post = create_post(text=request.data.get("text"), creator_id=request.data.get("creator_id"))
        serializer = PostSerializer(post)

        return Response(serializer.data)


class PostLikeViewSet(viewsets.ViewSet):
    def create(self, request):
        act = request.query_params.get("do_act")
        if act is None:
            raise APIException("Unexpected action")

        if act == "do_like":
            like = do_like(creator_id=request.data.get("creator_id"), post_id=request.data.get("post_id"))
            serializer = PostLikeSerializer(
                {
                    "creator_id": like.creator_id,
                    "is_liked": True,
                }
            )

            return Response(serializer.data)

        elif act == "do_unlike":
            do_unlike(creator_id=request.data.get("creator_id"), post_id=request.data.get("post_id"))
            serializer = PostLikeSerializer(
                {
                    "creator_id": request.data.get("creator_id"),
                    "is_liked": False,
                }
            )

            return Response(serializer.data)

        else:
            raise APIException("Unexpected action")
