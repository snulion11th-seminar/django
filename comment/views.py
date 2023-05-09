from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from post.models import Post
from post.serializers import PostSerializer
from .models import Comment
from .serializers import CommentSerializer


class CommentListView(APIView):
  
  
  def get(self, request):
    try:
      post_id=request.data.get('post')
    except:
      return Response({"detail": "missing fields['post]"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      commentlist=Comment.objects.filter(post_id=post_id).exists()
    except:
      return Response({"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(instance=commentlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

	### 2 ###
  def post(self, request):
    if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    content = request.data.get('content')
    post=request.data.get('post')

    if not content or not post:
      return Response({"detail": "missing fields ['post','content']"}, status=status.HTTP_400_BAD_REQUEST)

    postobject=Post.objects.filter(id=post)
    if not postobject.exists():
      return Response({"detail" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(content=content,post=postobject[0],author=request.user)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.auth:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        updated_content = request.data.get('content')
        
        if not updated_content:
            return Response({"detail": "missing fields [content]"}, status=status.HTTP_400_BAD_REQUEST)
          
        comment.content = updated_content
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
  def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.auth:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment.delete()
        return Response(status=status.HTTP_200_OK)
  

