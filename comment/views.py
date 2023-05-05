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
    if not 'post' in request.GET:
      return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
    post_id = request.GET['post'] 
    #쿼리파라미터를 url로부터 가져와야함, post는 게시물의 id번호였음
    try:
      Post.objects.get(id=post_id) #try: url로 받은 게시물 아이디와 같은 같은 아이디를 갖는 포스트를 가져와라!
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) #url로 받은 게시물 아이디가 없을때
    
    comments = Comment.objects.filter(post=post_id) 
    #코멘트마다 입력되어있는 post번호가 지금 받아온것과 같은것만 필터링 해서 가져와
    serializer = CommentSerializer(instance=comments, many=True)
    #구문 문법에 맞게 직렬화해서 저장
    print(post_id)
    return Response(serializer.data, status=status.HTTP_200_OK)


	### 2 ###
  def post(self, request):
    post_id = request.data.get('post')
    content = request.data.get('content')
    if not request.user.is_authenticated or request.user.is_anonymous:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
      author = request.user
    if not content or not post_id:
      return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
    try:
      post=Post.objects.get(id=post_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) #url로 받은 게시물 아이디가 없을때
    comment = Comment.objects.create(content=content,author=author,post=post)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
  def put(self, request, comment_id):
    content = request.data.get('content')
    if not content:
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
    if request.user.is_anonymous:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
      comment= Comment.objects.get(id=comment_id)
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
    if request.user.is_anonymous:
      return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
      comment= Comment.objects.get(id=comment_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.user != comment.author:
      return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
