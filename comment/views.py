from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from post.models import Post

class CommentListView(APIView):
    def get(self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comments = Comment.objects.filter(post=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentPostView(APIView):        
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        post = request.data.get('post')
        content = request.data.get('content')
        if not post or not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=post)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = Comment.objects.create(content=content, post=post, author=request.user)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):
    def put(self, request, comment_id):
        try:
            comments = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user != comments.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        content = request.data.get('content')
        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comments, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        try:
            comments = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user != comments.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
