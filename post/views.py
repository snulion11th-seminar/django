from django.shortcuts import render
from rest_framework.response import Response
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer

# Create your views here.

@api_view(['POST'])
def CreatePostView(request):
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
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
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
    
    def patch(self, request, post_id):
        title = request.data.get('title')
        content = request.data.get('content')
        if not (title and content) :
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not fount."}, status=status.HTTP_404_NOT_FOUND)
        
        if (post.title == title) or (post.content == content) :
            return Response({"detail": "Title or contents are same as before."}, status=status.HTTP_400_BAD_REQUEST)

        post.title=title
        post.content=content
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)