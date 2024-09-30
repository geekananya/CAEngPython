from rest_framework import serializers
from .models import Posts
from django.contrib.auth.models import User



# convert queryset -> python parsable data type to parsed to json
# similar syntax to django.forms

class PostSerializer(serializers.ModelSerializer):
    class Meta :
        model = Posts
        fields = '__all__'

    # def create(self, validated_data):
    #     author = User.objects.get(self.context['request'].user).id
    #     validated_data['author_id'] = author  # Set the author field
    #     return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'