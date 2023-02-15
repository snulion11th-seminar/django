from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    title = request.data['title']
    content = request.data['content']
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

#CBV without serializer
class PostListView(APIView):
    # allowed_method = ["POST"]
    def get(self, request):
        try:
            posts = Post.objects.all()
            contents = [{post.title:post.content} for post in posts]
            return Response(contents)
        except Exception as e:
            return Response({"error":e})

    def post(self, request):
        try:
            title = request.data['title']
            content = request.data['content']
            post = Post.objects.create(title=title, content=content)
            return Response({"msg":f"'{post.title}'이 생성되었어요!"})
        except Exception as e:
            return Response({"error":e})

class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return Response({"title":post.title, "content":post.content})
        except Exception as e:
            return Response({"error":e})

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            title = post.title
            post.delete()
            return Response({"msg":f"'{title}'이 삭제되었어요!"})
        except Exception as e:
            return Response({"error":e})

    # 과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.filter(id=post_id)
            if request.data['title'] :
                post.update(title=request.data['title'])
            if request.data['content'] :
                post.update(content=request.data['content'])
            return Response({"msg":"업데이트 되었습니다!"})
        except Exception as e:
            return Response({"error":e})


# CBV with serializer
class PostListView(APIView):
    def get(self, request):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error":e})

    def post(self, request):
        try:
            title = request.data['title']
            content = request.data['content']
            post = Post.objects.create(title=title, content=content)
            return Response({"msg":f"'{post.title}'이 생성되었어요!"})
        except Exception as e:
            return Response({"error" : e})

class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error":e})

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            title = post.title
            post.delete()
            return Response({"msg":f"'{title}'이 삭제되었어요!"})
        except Exception as e:
            return Response({"error":e})

    # 과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.filter(id=post_id)
            serializer = PostSerializer(post, data=request.data, partial=True)
            return Response({"msg":"업데이트 되었습니다!"})
        except Exception as e:
            return Response({"error":e})