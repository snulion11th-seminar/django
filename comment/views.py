from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import CommentSerializer

class CommentListView(APIView):
  def get(self, request):
    post_id = request.GET.get('post')
    if not post_id:
      return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
    comments = Comment.objects.filter(post_id=post_id)
    if not comments.exists():
      return Response({"detail": "Not found."}, status=status.HTTP_409_CONFLICT)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
        post = request.data.get('post')
        author = request.user
        content = request.data.get('content')
        if not author.is_authenticated:
          return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not post or not content:
            return Response({"detail": "missing fields [post, content]"}, status=status.HTTP_400_BAD_REQUEST)
        postobject = Post.objects.filter(id = post)
        if not postobject.exists:
          return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(content=content, post = postobject[0], author = author)
        serializer = CommentSerializer(comment)

        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):

  
  def put(self, request, comment_id):
      
      try:
        comment = Comment.objects.get(id=comment_id)
      except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
      if not request.user:
        return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
      if request.user != comment.author:
        return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
      content = request.data.get('content')
      if not content:
        return Response({"detail": "missing fields ['content']."}, status=status.HTTP_400_BAD_REQUEST)
      comment.content = content
      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=status.HTTP_200_OK)
  def delete(self, request, comment_id):
      try:
          comment = Comment.objects.get(id=comment_id)
      except:
          return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
      if request.user != comment.author:
          return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
