from urllib import response
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status

from comment.models import Comment
from comment.serializers import CommentSerializer
from post.models import Post

# Create your views here.
class CommentListView(APIView):
    def get(self, request):
        post_id = request.GET.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        comments = Comment.objects.filter(post_id=post_id)
        if not comments:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        author = request.user
        content = request.data.get('content')
        post_id = request.data.get('post')

        if not content or not post_id:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post=Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(author=author, content=content, post=post)
        serializer=CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):
    def put(self, request, comment_id):

        author = request.user
        content = request.data.get('content')
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        

        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment=Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author!=comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        comment.content=content
        comment.save()
        serializer=CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, comment_id):
        author = request.user
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            comment=Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author!=comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)