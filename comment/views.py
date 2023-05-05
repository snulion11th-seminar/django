from django.shortcuts import render
from .models import Comment
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import Post
from .serializers import CommentSerializer


# Create your views here.

class CommentCreateView(APIView):
    def post(self, request):
        author=request.user
        post = request.data.get('post')
        try:
            post_get = Post.objects.get(id=post)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        content=request.data.get('content')
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(author=author,content=content, post=post_get)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        post_id=request.GET.get('post')
        try:
            Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        if not post_id:
            return Response({"detail": "missing fields ['post']"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetailView(APIView):
    def put(self, request, comment_id):
        author = request.user
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        content=request.data.get('content')
        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        author = request.user
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            comment = Post.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
