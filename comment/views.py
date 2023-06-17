from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Post
from .serializers import CommentSerializer
from django.contrib.auth import get_user_model
from account.serializers import UserSerializer

User = get_user_model()


class CommentListView(APIView):
    def get(self, request):
        # 쿼리 파라미터에서 post_id 가져오기
        post_id = request.GET.get("post", None)

        # post_id가 없으면 400 Bad Request 반환
        if post_id is None:
            return Response(
                {"detail": "missing fields ['post']"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 주어진 post_id에 해당하는 Post 객체 가져오기
        try:
            post = Post.objects.get(id=post_id)

        # Post 객체를 찾을 수 없으면, 404 Not Found 반환
        # DoesNotExist는 Django에서 사용하는 예외입니다.
        # 이 예외는 get() 쿼리 메소드를 사용하여 특정 모델 객체를 조회하려고 할 때, 일치하는 객체를 찾을 수 없는 경우 발생합니다.
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # 포스트와 관련된 댓글을 필터링합니다.
        comments = Comment.objects.filter(post=post)

        # 댓글을 직렬화합니다.
        serializer = CommentSerializer(instance=comments, many=True)

        # 직렬화된 댓글과 함께 200 OK 상태를 반환합니다.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        post_id = request.data.get("post")
        content = request.data.get("content")

        if not post_id or not content:
            return Response(
                {"detail": "missing fields ['post', 'content']"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(
            post=post, content=content, author=request.user
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, comment_id):
        # request user가 authenticated가 아닌 경우, 401 Unauthorized 반환
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # comment_id에 해당하는 Comment 객체 가져오기
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # request user가 comment author가 아닌 경우, 401 Unauthorized 반환
        if request.user != comment.author:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # request data로 CommentSerializer를 통해 Comment 객체 업데이트
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        # 업데이트 된 Comment 객체를 직렬화하여 반환
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != comment.author:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = CommentSerializer(
            comment, data=request.data, partial=True
        )  # Allow partial updates
        if not serializer.is_valid():
            return Response(
                {"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
