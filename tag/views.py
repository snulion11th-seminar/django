from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer

from post.models import Post
from post.serializers import PostSerializer


class TagListView(APIView):
    ### 1 ###
    def get(self, request):
        tags = Tag.objects.all()
        # 태그가 여러개가 있을 수 있기 때문에 serializer를 many=True(여러개라는 옵션)로 해줘야함.
        serializer = TagSerializer(instance=tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    ### 2 ###
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # content는 model 에 정의되어있는 내용임. 태그 안에 들어가는 내용을 content라고 정의했음.
        content = request.data.get("content")

        if not content:
            return Response(
                {"detail": "missing fields ['content']"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Tag.objects.filter(content=content).exists():
            return Response(
                {"detail": "Tag with same content already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        tag = Tag.objects.create(content=content)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagDetailView(APIView):
    def get(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response(
                {"detail": "Provided tag does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        posts = Post.objects.filter(tags=tag)  # Filter posts based on the tag
        serializer = PostSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response(
                {"detail": "Provided tag does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Verify if the user is authenticated before deleting the tag
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Delete the tag
        tag.delete()
        return Response(
            {"detail": "Tag deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
