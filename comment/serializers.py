from rest_framework.serializers import ModelSerializer
from .models import Comment
from account.serializers import UserIdUsernameSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        
    author = UserIdUsernameSerializer(read_only = True)