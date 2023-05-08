from django.shortcuts import render
from rest_framework.response import Response
from .models import Post, Like
from rest_framework.decorators import api_view
from tag.models import Tag

@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title') # request body로 보낸 정보를 python dictionary로 바꿔주고 get으로 value를 가져옴. 
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content) #앞 title이 db 속 column 이름, 뒤 title이 get한 value. 
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response({"posts":contents})

from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer

class PostListView(APIView):		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all().order_by('-like_users')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)      
  
    def post(self, request):
        author = request.user
        tag_ids = request.data.get('tags')
        title = request.data.get('title')
        content = request.data.get('content')
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not title or not content: # 미리 예상되는 문제에 대해서 분기 처리를 해두는 것이 좋다. 
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        for tag_id in tag_ids:
            if not Tag.objects.filter(id=tag_id).exists():
                return Response({"detail": "Provided tag not found."}, status=status.HTTP_404_NOT_FOUND)
        post = Post.objects.create(title=title, content=content, author=author) # author 정보도 담아주쇼
        post.tags.set(tag_ids)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.utils import timezone

class PostDetailView(APIView):
    def get(self, request, post_id): # post_id를 받아오기 시작함 <= 특정 object에 접근하고 싶기 때문..! -> url 뒤에 id를 붙이게 됨요
        try: #try-except 구문
            post = Post.objects.get(id=post_id) #quertyset
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

    def patch(self, request, post_id):
        try: #try-except 구문
            post = Post.objects.get(id=post_id) #quertyset
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        title = request.data.get('title')
        content = request.data.get('content')
        if title:
            if title == post.title:
                return Response({"Nothing to Update"})
            post.title = request.data.get('title')
        if content:
            if content == content.title:
                return Response({"Nothing to Update"})
            post.content = request.data.get('content')
        post.updated_at = timezone.localtime()
        post.save()
        serializer = PostSerializer(post)
        return Response({"Success to Update!"}, status=status.HTTP_200_OK)
    
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
            post.like_set.get(user=request.user).delete() # 이미 눌렀으면 좋아요 취소
        else:
            Like.objects.create(user=request.user, post=post) # 누른 적 없으니까 좋아요 & 좋아요 카운트++

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)