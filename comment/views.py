from django.shortcuts import render
from rest_framework.response import Response
from .models import Comment
from post.models import Post

from rest_framework.views import APIView
from rest_framework import status
from .serializers import CommentSerializer

# Create your views here.

class CommentListView(APIView):
  def get(self,request):
    post_id = request.GET.get("post")
    if not post_id:
      return Response({"detail" : "missing fields ['post']"} , status=status.HTTP_400_BAD_REQUEST)
    try:
      post = Post.objects.get(id = post_id)
    except:
      return Response({"detail" : "Not found."},status=status.HTTP_404_NOT_FOUND)
    comments = Comment.objects.filter(post = post)
    serializer = CommentSerializer(instance = comments, many =True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  
  def post(self,request):
    post_id = request.data.get("post")
    content = request.data.get("content")
    author = request.user
    if not author.is_authenticated:
      return Response({"detail" : "Authentication credentials not provided"})
    if not (post_id and content):
      return Response({"detail" : "missing fields ['post', 'content']"},status=status.HTTP_400_BAD_REQUEST)
    try:
      post = Post.objects.get(id = post_id)
    except:
      return Response({"detail":"Not found."},status=status.HTTP_404_NOT_FOUND)
    comment = Comment.objects.create(post=post,author = author,content=content)    
    serializer = CommentSerializer(comment)
    return Response(serializer.data,status=status.HTTP_201_CREATED)  
  
  
class CommentDetailView(APIView):
  def put(self,request,comment_id):
    if not request.user.is_authenticated:
      return Response({"detail" : "Authentication credentials not provided"},status=status.HTTP_401_UNAUTHORIZED)
    try:
      comment = Comment.objects.get(id = comment_id)
    except:
      return Response({"detail" : "Not found."},status=status.HTTP_404_NOT_FOUND)
    if not comment.author == request.user:
      return Response({"detail" : "Permission denied"},status=status.HTTP_401_UNAUTHORIZED)
    new_content = request.data.get("content")
    if not new_content:
      return Response({"detail":"missing fields ['content']"},status=status.HTTP_400_BAD_REQUEST)
    comment.content = new_content
    comment.save()
    serializer = CommentSerializer(comment)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  def delete(self, request,comment_id):
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"},status=status.HTTP_401_UNAUTHORIZED)
    try:
      comment = Comment.objects.get(id = comment_id)
    except:
      return Response({"detail" : "Not found."},status=status.HTTP_404_NOT_FOUND)
    
    if request.user != comment.author:
      return Response({"detail" : "Permission denied"},status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)