from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response

# rest_framework의 response에 가서 Response 를 임포트해라는 뜻.

from .models import Post
from rest_framework.decorators import api_view



@api_view(['POST'])
def CreatePostView(request):
    """
    request 를 보낼 때 post 의 title 과 content 를 보내야합니다.
    """
    title = request.data.get('title')
    # request.data 는 바디에 있는 데이터를 파이썬 용어로 바꿔주고 get 안에 있는 걸 밸류로 가져온다.
    content = request.data.get('content')
    id = request.data.get('id')
    post = Post.objects.create(id=id, title=title, content=content)
      # Post라는 모델의 objects를 만들겟다. title은 title, content는 content. title=title에서 앞에꺼는 키값, 뒤에꺼는 바로 위에 적은 거
    return Response({"msg":f"'{post.title}'이 생성되었어요!"})
      # 문자열 하나를 만들건데, 이런 변수를 넣어서 만들겠다. 문자열이랑 변수랑 같이 쓸때 f string 활용함.

@api_view(['GET'])
def ReadAllPostView(request):
    posts = Post.objects.all()
    titles = [{post.title} for post in posts]
    contents = [{post.content} for post in posts]
    ids = [post.id for post in posts]
      # post의 title과 content를 딕셔너리로 만들어서 리스트에 넣어준다.
    return Response({"제목": titles, 
                    "내용": contents, 
                    "id": ids})


@api_view(['GET'])
def ReadSpecificPostView(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
    return Response({"title": post.title, "content": post.content, "id": id})


@api_view(['PUT'])
def UpdatePostView(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    title = request.data.get('title')
    content = request.data.get('content')

    if title is not None:
        post.title = title

    if content is not None:
        post.content = content

    post.save()

    return Response({"msg": f"'{post.title}'이 업데이트되었어요!"})


# ####아래는 cbv 방식으로 바꾼 것.####

# class PostListView(APIView):

# 		### 얘네가 class inner function 들! ###
#     def get(self, request): 
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # contents = [{"id":post.id,
#         #              "title":post.title,
#         #              "content":post.content,
#         #              "created_at":post.created_at
#         #              } for post in posts]
#         # return Response(contents, status=status.HTTP_200_OK)
        

#     def post(self, request):
#         title = request.data.get('title')
#         content = request.data.get('content')
#         if not title or not content:
#             return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
# ### 이거 하는 이유는 미리 대처할 수 있는 거를 분기처리해주는 것. ###
#         post = Post.objects.create(title=title, content=content)
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response({
#         #     "id":post.id,
#         #     "title":post.title,
#         #     "content":post.content,
#         #     "created_at":post.created_at
#         #     }, status=status.HTTP_201_CREATED)
    
#     ##위에 뷰는 listview, 아래 뷰는 detailview.##
#     ##아래는 특정 게시글에 접근하는 view.##
#     ##listView랑 다른 점은, Get 요청 뒤에 post id 를 받아오는 것.
#     ## 특정한 오브젝트에 접근한다고 했음. 이 View 는 url 통해서 호출되고 url에다가 번호를 붙일 것임. 그 id가 url에 들어가서 아이디로 들어오는 것
#     ## 그래서 get, delete 메소드에 post_id를 받아오는 것. 그리고 그 post_id를 가지고 있는 게시글을 찾아서 post에 넣어준다.
#     ## try except로 에러처리를 해준다.

# class PostDetailView(APIView):
#     def get(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#         except:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#         return Response({
#             "id":post.id,
#             "title":post.title,
#             "content":post.content,
#             "created_at":post.created_at
#             }, status=status.HTTP_200_OK)
        
#     def delete(self, request, post_id):
#         try:
#             post = Post.objects.get(id=post_id)
#         except:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)