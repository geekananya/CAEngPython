from rest_framework import serializers
from .models import Posts, Likes
from django.contrib.auth.models import User

# convert queryset -> python parsable data type to parsed to json
# similar syntax to django.forms

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.PrimaryKeyRelatedField(read_only=True)  # Make it read-only

    class Meta :
        model = Posts
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author_username'] = (self.context['author'])
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['post_id', 'user_id']