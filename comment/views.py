from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer
from post.models import Post


class CommentListView(APIView):
	### 1 ###
  def get(self, request):

    post_id = request.GET.get('post')
    if not post_id:
      return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
    
    comments = Comment.objects.filter(post_id=post_id)
    if not Post.objects.filter(id=post_id).exists():
      return Response({"detail" : "Not found."}, status=status.HTTP_404_NOT_FOUND)
  
    serializer = CommentSerializer(instance=comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

	### 2 ###
  def post(self, request):
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
  
    author = request.user
    post_id = request.data.get('post')
    content = request.data.get('content')

    if not author.is_authenticated:
        return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    if not content or not post_id:
      return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not Post.objects.filter(id=post_id).exists():
      return Response({"detail" : "Not found."}, status=status.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(author=author, post_id=post_id, content=content)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  ##Only for revision
  ##3
  def put(self, request, comment_id):

    comment = Comment.objects.get(id=comment_id)

    if not request.data.get('content'):
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not request.user.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user != comment.author:
        return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not comment:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({"detail": "data validation error"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  ##4
  def delete(self, request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != comment.author:
        return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)