from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Count
from tag.models import Tag

from .models import Like, Post
from .serializers import PostSerializer


class PostListView(APIView):
    def get(self, request):
        posts = (
            Post.objects.all()
            .annotate(like_count=Count("like_users"))
            .order_by("-like_count")
        )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        author = request.user
        title = request.data.get("title")
        content = request.data.get("content")
        tag_contents = request.data.get("tags")

        if not author.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not title or not content:
            return Response(
                {"detail": "[title, description] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post = Post.objects.create(title=title, content=content, author=author)

        for tag_content in tag_contents:
            if not Tag.objects.filter(content=tag_content).exists():
                post.tags.create(content=tag_content)
            else:
                post.tags.add(Tag.objects.get(content=tag_content))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": {"username": post.author.username, "id": post.author.id},
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user != post.author:
            return Response(
                {"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED
            )

        print(request.data)
        serializer = PostSerializer(
            post, data=request.data, partial=True, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                {"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(APIView):
    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # 2
        like_list = post.like_set.filter(user=request.user)
        liked = False
        # 3 like_list.count() > 0 이라는 말은, like_list가 존재한다는 말. 즉, 좋아요를 누른 적이 있다는 말.
        # 그래서 delete를 해준다. (왜냐하면 좋아요 한 사람이 버튼을 눌렀다는 건 취소하고 싶다는 뜻이니까)
        # Else는 반대라서 create 해주는 것
        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        serializer = PostSerializer(instance=post)
        data = serializer.data
        data["liked"] = liked

        return Response(data, status=status.HTTP_200_OK)
