from django.utils import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

from tag.models import Tag
from .serializers import PostSerializer
from .models import Like, Post

@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

# 아래에 추가해주세요! 
@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response({"posts":contents})

...
from rest_framework.views import APIView
from rest_framework import status
...

class PostListView(APIView):

		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all()
        # contents = [{"id":post.id,
        #              "title":post.title,
        #              "content":post.content,
        #              "created_at":post.created_at
        #              } for post in posts]
        # return Response(contents, status=status.HTTP_200_OK)
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        author = request.user
        title = request.data.get('title')
        content = request.data.get('content')
        tag_contents = request.data.get('tags')


        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not title or not content:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        post = Post.objects.create(title=title, content=content, author=author)
        for tag_content in tag_contents:
            if not Tag.objects.filter(content=tag_content).exists():
                post.tags.create(content=tag_content)
            post.tags.add(Tag.objects.get(content=tag_content))
                # return Response({"detail": "Provided tag not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response({"detail": "You are not the author of this post."}, status=status.HTTP_401_UNAUTHORIZED)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(post, data=request.data, partial=True)
				
				## 수정

        tag_contents = request.data.get("tags")
        #tag 쪽 없으면 create 있으면 add
        post.tags.clear()  # 처음에는 clear
        for tag_content in tag_contents:
            if not Tag.objects.filter(
                content=tag_content
            ).exists():  
                post.tags.create(content=tag_content)
            post.tags.add(Tag.objects.get(content=tag_content))

        ## 수정
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
        like_list = post.like_set.filter(user=request.user)

        ### 3 ###
        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)