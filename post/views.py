from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt



from rest_framework.response import Response
from .models import Post

@csrf_exempt
@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title')
    content = request.data.get('content')
    post = Post.objects.create(title=title, content=content)
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})

@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    contents = [{post.title:post.content} for post in posts]
    return Response({"posts":contents})

# @api_view(['PUT'])
# def UpdatePostView(request):
#     title = request.data.get('title')
#     content = request.data.get('content')
#     post = Post.objects.put(title=title, content=content)
#     return Response({"msg":f"'{post.title}'이 수정되었어요!"})



from rest_framework.views import APIView
from rest_framework import status


# class PostListView(APIView):

# 		### 얘네가 class inner function 들! ###
#     def get(self, request): 
#         posts = Post.objects.all()
#         contents = [{"id":post.id,
#                      "title":post.title,
#                      "content":post.content,
#                      "created_at":post.created_at
#                      } for post in posts]
#         return Response(contents, status=status.HTTP_200_OK)
        

#     def post(self, request):
#         title = request.data.get('title')
#         content = request.data.get('content')
#         if not title or not content:
#             return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
#         post = Post.objects.create(title=title, content=content)
#         return Response({
#             "id":post.id,
#             "title":post.title,
#             "content":post.content,
#             "created_at":post.created_at
#             }, status=status.HTTP_201_CREATED)
    

from .serializers import PostSerializer


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
#### 수정 ###
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#### 여기까지 ###

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
#### 수정 ###
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#### 여기까지 ###

    # class PostDetailView(APIView):
    #   def get(self, request, post_id):
    #       try:
    #           post = Post.objects.get(id=post_id)
    #       except:
    #           return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    #       return Response({
    #           "id":post.id,
    #           "title":post.title,
    #           "content":post.content,
    #           "created_at":post.created_at
    #           }, status=status.HTTP_200_OK)
        
    #   def delete(self, request, post_id):
    #       try:
    #           post = Post.objects.get(id=post_id)
    #       except:
    #           return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    #       post.delete()
    #       return Response(status=status.HTTP_204_NO_CONTENT)

class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
    # def put(self, request, post_id):
    #    try:
    #        post = Post.objects.get(id=post_id)
    #    except:
    #        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    #    ##title = request.data.get('title')
    #    ##content = request.data.get('content')
    #    ##post = post.objects.put(title=title, content=content)

    #    serializer = PostSerializer(post, request.data)
    #    if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        title = request.data.get('title')
        content = request.data.get('content')
        post = post.objects.update(title=title, content=content)


    
       
