from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import Post, Like
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import PostSerializer
from tag.models import Tag
from django.db.models import Count

@csrf_exempt
@api_view(['POST'])
def CreatePostView(request):
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

@csrf_exempt
@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response({"posts":contents})

from rest_framework.views import APIView
from rest_framework import status

class PostListView(APIView):
    def get(self, request): 
        posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')
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
        post.tags.set(tag_ids)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        post.title = request.data.get('title')
        post.content = request.data.get('content')
        serializer = PostSerializer(post)
        return Response(serializer.data)

class LikeView(APIView):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        like_list = post.like_set.filter(user=request.user)

        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)
