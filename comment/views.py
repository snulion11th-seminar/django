from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from comment.serializers import CommentSerializer
from post.models import Post
from .models import Comment
from rest_framework.views import APIView

class CommentListView(APIView):
    def get(self, request):
        query = request.GET['post']
        if not query:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comments = Comment.objects.filter(post_id=query)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        try:
            post = Post.objects.get(id=request.data.get('post'))
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        content = request.data.get('content')
        author = request.user


        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        if not post or not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(post=post, content=content, author=author)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentDetailView(APIView):
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


