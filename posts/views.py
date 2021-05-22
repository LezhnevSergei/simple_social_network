from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from posts.serializers import PostSerializer, PostLikeSerializer
from posts.services import create_post, get_posts, get_post, do_like, do_unlike, delete_post


class PostViewSet(viewsets.ViewSet):
    def retrieve(self, request, post_id: int, *args, **kwargs):
        post = get_post(post_id=post_id, current_user_id=request.user.id)
        serializer = PostSerializer(post)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        posts = get_posts(current_user_id=request.user.id)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        post = create_post(text=request.data.get("text"), creator_id=request.user.id)
        serializer = PostSerializer(post)

        return Response(serializer.data)

    def destroy(self, request, pk: int):
        delete_post(post_id=pk, user_id=request.user.id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        act = request.query_params.get("do_act")
        if act is None:
            raise APIException("Unexpected action")

        if act == "like":
            like = do_like(creator_id=request.user.id, post_id=request.data.get("post_id"))
            serializer = PostLikeSerializer(
                {
                    "creator_id": like.creator_id,
                    "is_liked": True,
                }
            )

            return Response(serializer.data)

        elif act == "unlike":
            do_unlike(creator_id=request.user.id, post_id=request.data.get("post_id"))
            serializer = PostLikeSerializer(
                {
                    "creator_id": request.user.id,
                    "is_liked": False,
                }
            )

            return Response(serializer.data)

        else:
            raise APIException("Unexpected action")
