from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt

from .models import Post
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.all()
        contents = [{"id":post.id,
                     "title":post.title,
                     "content":post.content,
                     "created_at":post.created_at
                     } for post in posts]
        return Response(contents, status=status.HTTP_200_OK)
        

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post = Post.objects.create(title=title, content=content)
            return Response({
                "id":post.id,
                "title":post.title,
                "content":post.content,
                "created_at":post.created_at
                }, status=status.HTTP_201_CREATED)

        

class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "id":post.id,
            "title":post.title,
            "content":post.content,
            "created_at":post.created_at
            }, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
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
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content :
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post.update(title=title, content=content)
            return Response({
                "id":post.id,
                "title":post.title,
                "content":post.content,
                "created_at":post.created_at
                }, status=status.HTTP_200_OK)
        
        


# CBV with serializer
class PostListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post = Post.objects.create(title=title, content=content)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # 과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)