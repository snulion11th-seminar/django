from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer
from post.models import Post
from post.serializers import PostSerializer

class CommentCreateView(APIView):
  def get(self, request):
    try: 
      comments = Comment.objects.filter(post=request.GET.get('post')) #quertyset
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  def post(self, request):
    try: #try-except 구문
            post = Post.objects.get(id=request.data.get('post')) #quertyset
    except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    author = request.user
    content = request.data.get('content')
    if not author.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    if not post or not content:
      return Response({"detail": "[post, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.create(content=content, author=author, post=post)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
  def patch(self, request, comment_id):
    try: #try-except 구문
            comment = Comment.objects.get(id=comment_id) #quertyset
    except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    author = request.user
    content = request.data.get('content')
    if not author.is_authenticated:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    if not content:
      return Response({"detail": "[content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    if request.user != comment.author:
      return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.content = request.data.get('content')
    comment.save()
    serializer = CommentSerializer(comment)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_200_OK)
  def delete(self, request, comment_id):
    try: #try-except 구문
            comment = Comment.objects.get(id=comment_id) #quertyset
    except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
