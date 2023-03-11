from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Post
from seminar.helpers import CSRFExemptView
from django.http import JsonResponse

from .serializers import PostSerializer


# FBV
@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response(contents)

@csrf_exempt
@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

#CBV without serializer
class PostListView(APIView):
    # allowed_method = ["POST"]
    def get(self, request):
        posts = Post.objects.all()
        contents = [{post.title:post.content} for post in posts]
        return Response(contents)
        

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if title and content:
            post = Post.objects.create(title=title, content=content)
            return Response({"msg":f"'{post.title}'이 생성되었어요!"})
        else:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)

        

class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return Response({"title":post.title, "content":post.content})
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        title = post.title
        post.delete()
        return Response({"msg":f"'{title}'이 삭제되었어요!"})
        

    # 과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.filter(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        title = request.data.get('title')
        content = request.data.get('content')
        if title and content :
            post.update(title=request.data['title'], content=request.data['content'])
            return Response({"msg":"업데이트 되었습니다!"})
        else:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        


# CBV with serializer
class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if title and content:
            post = Post.objects.create(title=title, content=content)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)

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
            title = post.title
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # 과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)