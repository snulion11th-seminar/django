from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Post, Like
from .serializers import PostSerializer

class PostListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        author = request.user
        tags = request.data.get('tags')
        if not title or not content:
            return Response({"detail": "[title, description] fields missing."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO auth
        post = Post.objects.create(title=title, content=content, author=author)
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
        # TODO auth
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #과제
    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # TODO auth
        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# 7th week(ManyToMany Field_Like)
class LikeView(APIView):
    def get(self, request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(instance=post)
            like_list = post.like_set.filter(user_id=request.user.id).all()
            if like_list.count() > 0:
                post.like_set.get(user=request.user).delete()
            else:
                Like.objects.create(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
