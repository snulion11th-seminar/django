from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from post.models import Post
from .models import Comment

# Create your views here.
    

class CommentListView(APIView) :
    def get(self, request) :
        # 1. Check if post_id exists
        if not 'post' in request.GET :
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
    
        # 2. try to GET comments of the post_id
        try:
            post_id = request.GET.get('post')
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comments_list = post.comment_set.all()
        serializer = CommentSerializer(instance=comments_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) :
        # 1. check if user is authorized
        author = request.user
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 2. check data
        # 2 - 1. check if post_id, content exist
        post_id = request.data.get('post')
        content = request.data.get('content')
        if not (post_id and content) :
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2 - 2. check if post_id is valid
        try :
            Post.objects.get(id=post_id)
        except :
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 3. create new comment
        comment = Comment.objects.create(post_id=post_id, content=content, author=author)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView) :
    def put(self, request, commentId) :
        # 1. Check if commentId is valid
        try :
            comment = Comment.objects.get(id=commentId)
        except :
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 2. Check if the token exists
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        # 3. Check if the user is authorized(same as writer)
        if comment.author != request.user :
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 4. Check if the data is not empty
        content = request.data.get('content')
        if not content :
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 5. update
        comment.content=content
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, commentId) :
        # 1. Check if commentId is valid
        try :
            comment = Comment.objects.get(id=commentId)
        except :
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 2. Check if the token exists
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 3. Check if the user is authorized(same as writer)
        if comment.author != request.user :
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 4. delete
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

