from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comment.models import Comment
from comment.serializers import CommentSerializer

from post.models import Post

class CommentListView(APIView):
  def get(self, request):
    post_id = request.GET.get('post')
    try:
      post = Post.objects.get(id=post_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    comment_list = post.comment_set.all()
    serializer = CommentSerializer(comment_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    author = request.user
    post_id = request.data.get('post')
    content = request.data.get('content')

    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not post_id or not content:
      return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      selected_post = Post.objects.get(id=post_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    comment = Comment.objects.create(post=selected_post, content=content, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
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
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

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