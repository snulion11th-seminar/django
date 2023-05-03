from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer

from post.models import Post
from post.serializers import PostSerializer


class CommentListView(APIView):
	### 1 ###
  def get(self, request):
    post_id = request.GET.get('post')

    if not post_id:
      return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      Post.objects.get(id=post_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(instance=comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

	### 2 ###
  def post(self, request):
    if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    
    author = request.user
    post_id = request.data.get('post')
    content = request.data.get('content')

    if not (post_id and content):
      return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      post = Post.objects.get(id=post_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(content=content, post=post, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
  def patch(self, request, comment_id):
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    content = request.data.get('content')

    if not content:
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user != comment.author:
      return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    
    if not serializer.is_valid():
        return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
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
