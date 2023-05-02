from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
from .models import Comment
from post.models import Post
from .serializers import CommentSerializer

# Create your views here.
class CommentListView(APIView):
  def get(self, request):
    try:
        post_id = request.GET.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
  
  def post(self,request):
      author = request.user
      if not author.is_authenticated:
        return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
      post_id = request.data.get('post')
      if not Post.objects.filter(id=post_id).exists():
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
      content = request.data.get('content')
      if not post_id or not content:
        return Response({"detail": "[post, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
      comment = Comment.objects.create(post = Post.objects.get(id=post_id), content=content, author = author)
      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
  
class CommentDetailView(APIView):
  def put(self, request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user != comment.author:
      return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.content = request.data.get('content')
    if not comment.content :
      return Response({"detail": "missing fields ['content']"}) 
    serializer = CommentSerializer(comment)
    if not Comment.objects.filter(id=comment_id).exists():
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data,status=status.HTTP_200_OK)
  

  def delete(self, request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user != comment.author:
      return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.content = request.data.get('content') 
    if not Comment.objects.filter(id=comment_id).exists():
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  


    