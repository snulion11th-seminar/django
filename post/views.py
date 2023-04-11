from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import Post
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework import status

from .serializers import PostSerializer


@api_view(['POST'])
def CreatePostView(request):
    title = request.data.get('title')
    content = request.data.get('content')
    # Object-Relational Mapping
    post = Post.objects.create(title=title, content=content)
    return Response({"msg": f"'{post.title}'이 생성되었어요!"})

# 아래에 추가해주세요!


@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()  # DB에 저장된 모든 게시글의 정보를 가져와서 list로 만들어줌
    contents = [{post.title: post.content} for post in posts]
    return Response({"posts": contents})

# object의 id가 필요하지 않은 경우 -> 불특정 다수에 집중하는 경우


class PostListView(APIView):

    ### 얘네가 class inner function 들! ###
    def get(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # contents = [{"id": post.id,
        #              "title": post.title,
        #              "content": post.content,
        #              "created_at": post.created_at
        #              } for post in posts]
        # return Response(contents, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        # PostSerializer(instance, data) -> data는 Request, instance는 db에 있는 것.
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at
        }, status=status.HTTP_201_CREATED)


# object의 id가 필요한 경우 -> 특정한 게시글에 접근
class PostDetailView(APIView):
    def get(self, request, post_id):
        print(request)
        print(request.data)
        try:
            post = Post.objects.get(id=post_id)
            print(post)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # return Response({
        #     "id": post.id,
        #     "title": post.title,
        #     "content": post.content,
        #     "created_at": post.created_at
        # }, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            print(post)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # print(request.data)

        post.content = request.data.get('content', post.content)
        post.title = request.data.get('title', post.title)

        post.objects.update(title=post.title, content=post.content)
        print(post)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # serializer = PostSerializer(post, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     # print(serializer.data)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
