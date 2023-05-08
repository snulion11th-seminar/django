from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Comment, Post
from .serializers import CommentSerializer

# Create your views here.
class CommentListView(APIView):

    def get(self, request): 
        try:
            post_id = request.GET.get('post')
        except:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        author = request.user
        post_id = request.data.get('post')
        content = request.data.get('content')
        
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not author or not content:
            return Response({"detail": "[author, comment] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.create(content=content, post=post, author=author)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):
    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, comment_id):
        author = request.user
        if not author.is_authenticated:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, comment_id):
        try:
            request.COOKIES.get('access_token')
        except:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        author = request.user
        if not author.is_authenticated:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        if comment.author != author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            comment.content = request.data['content']
            comment.save()
        except:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        # comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
