from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post

from .models import Comment
from .serializers import CommentSerializer


# Create your views here.
class CommentListView(APIView):
    def get(self, request):
        post_id = request.data.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comments = Comment.objects.get(post_id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # TODO auth
        author = request.user
        post_id = request.data.get('post')
        content = request.data.get('content')

        if not post_id or not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(Post.objects.filter(post_id=post_id)) == 0:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = Comment.objects.create(post_id=post_id, author=author, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    def patch(self, request, comment_id):
        # TODO auth
        content = request.data.get('content')
        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.filter(id=comment_id)
        if len(comment) == 0:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comment[0], data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        # TODO auth
        comment = Comment.objects.filter(id=comment_id)
        if len(comment) == 0:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        