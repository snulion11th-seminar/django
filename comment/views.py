from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Post
from .serializers import CommentSerializer


# Create your views here.
class CommentListView(APIView):
    #코멘트 보기
    def get(self, request):

      post_id = request.GET.get("post")
      if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)

      try:
          comments = Comment.objects.filter(post=post_id)
          
      except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
      
      serializer = CommentSerializer(instance=comments, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    #코멘트 달기
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        content = request.data.get('content')
        post_id = request.data.get('post_id')
      
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not content or not post:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(post=post, content=content, author=request.user)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    #코멘트 업데이트
    def put(self, request, comment_id):
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        content = request.data.get('content')      
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #코멘트 삭제
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