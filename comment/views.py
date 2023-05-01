from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post

from .models import Comment
from .serializers import CommentSerializer

class CommentListView(APIView):
  
  def get(self, request):
    post_id = request.GET.get('post', None)

    if post_id == None:
        return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    print(post.comment_set)
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(instance=comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        

  def post(self, request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    author = request.user
    post = request.data.get('post')
    content = request.data.get('content')

    if not content:
        return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)

    if not Post.objects.filter(id=post).exists():
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
    comment = Comment.objects.create(post=Post.objects.get(id=post), content=content, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
    
    def delete(self, request, comment_id):
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, comment_id):
        
        content = request.data.get('content')
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if not content:
          return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment.content = content
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)