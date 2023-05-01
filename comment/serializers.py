from rest_framework.serializers import ModelSerializer
from account.serializers import UserIdUsernameSerializer

from .models import Comment

class CommentSerializer(ModelSerializer):
	
    author = UserIdUsernameSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = "__all__"