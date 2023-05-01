from django.shortcuts import render
from .models import Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from .models import Post


class CreateCommentView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        ### 1 ###
        try:
            post = Post.objects.get(id=request.data.get('post'))
        except:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get('content')

        if not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            author=request.user, content=content, post=post)

        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        try:
            post = Post.objects.get(id=int(request.GET.get('post')))
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not post:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)

        comment_list = Comment.objects.filter(
            post_id=int(request.GET.get('post')))

        serializer = CommentSerializer(comment_list, many=True)
        # serializer = PostCommentSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCommentView(APIView):
    def put(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.content = request.data.get('content')

        if comment.content:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
