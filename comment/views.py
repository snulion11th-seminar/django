from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

# Create your views here.
class CommentListView(APIView):

    def get(self, request): 
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        author = request.data.get('author')
        comment = request.data.get('comment')
        if not author or not comment:
            return Response({"detail": "[author, comment] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(author=author, comment=comment)
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
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # comment.author = request.data.get('author')
        # comment.comment = request.data.get('comment')
        try:
            comment.author = request.data.get('author')
            comment.comment = request.data.get('comment')
            comment.save()
        except:
            return Response({"detail": "[author] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        # comment.save()
        return Response({
    "id":comment.id,
    "author":comment.author,
    "comment":comment.comment,
    "created_at":comment.created_at
    }, status=status.HTTP_200_OK)
    
    def patch(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment.author = request.data.get('author') or comment.author
        comment.comment = request.data.get('comment') or comment.comment
        comment.save()
        return Response({
    "id":comment.id,
    "author": comment.author,
    "comment": comment.comment,
    "created_at": comment.created_at
    }, status=status.HTTP_200_OK)