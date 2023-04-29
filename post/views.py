from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import Post, Like
from .serializers import PostSerializer
from tag.models import Tag

@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response({"posts":contents})

class PostListView(APIView):

		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        author = request.user
        title = request.data.get('title')
        content = request.data.get('content')
        tag_ids = request.data.get('tags')
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        for tag_id in tag_ids:
            if not Tag.objects.filter(id=tag_id).exists():
                return Response({"detail": "Provided tag not found."}, status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.create(title=title, content=content, author=author)
        post.tags.set(tag_ids) # post와 tag를 연결(django 자동 중계 테이블 연결)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # post.title = request.data.get('title')
        # post.content = request.data.get('content')
        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            post.title = request.data.get('title')
            post.content = request.data.get('content')
            post.save()
        except:
            return Response({"detail": "[title] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        # post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        post.title = request.data.get('title') or post.title
        post.content = request.data.get('content') or post.content
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LikeView(APIView):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        ### 2 ###
        like_list = post.like_set.filter(user=request.user) # post에서 like table에 like_set으로 역참조

        ### 3 ###
        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete() # 좋아요 취소
        else:
            Like.objects.create(user=request.user, post=post) # 좋아요 생성

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)