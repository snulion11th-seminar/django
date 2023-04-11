from django.shortcuts import render

from rest_framework.response import Response
from .models import Post
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PostSerializer

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def CreatePostView(request):
    """
    request
    """
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}' is made!"})

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
        post = Post.objects.create(title=title, content=content)#cf)create = make + save(no need to save)
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
    
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "id":post.id,
            "title":request.data.get('title'),
            "content":request.data.get('content'),
            "created_at":post.created_at
            }, status=status.HTTP_200_OK)

    
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)