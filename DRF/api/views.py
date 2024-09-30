from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Posts
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer


# this guy implemented his own login/register functions, and utilised drf tokens to generate tokens and verify/validate them
# and django user model to automatically hash password (but we can use an external lib for that for custom user model)



@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data.get('username'))
    if not user.check_password(request.data.get('password')):
        return Response({"detail": "Invalid Credentials", "status": status.HTTP_400_BAD_REQUEST})
    print(user.username) # Replace with the correct user ID
    user.is_active = True
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    serialiser = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serialiser.data})


@api_view(['POST'])
def register(request):
    serialiser = UserSerializer(data=request.data)  # convert to python parsable (we send this in resp)
    # print(request.data)
    if serialiser.is_valid():
        serialiser.save()
        user = User.objects.get(email=request.data.get('email'))  # no need to be parsed by python, db purpose only
        user.set_password(request.data.get('password'))  # hashes password
        user.save()
        print(user.password)
        token = Token.objects.create(user=user)
        print(token)
        return Response({'token': token.key, 'user': serialiser.data})
    return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist) as e:
        print(e)
    return Response({"success": "Successfully logged out."},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def welcome(request):
    return Response({"msg": "Welcome to django rest api"})


@api_view(['GET'])
def get_posts(request):
    posts = Posts.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# protected route
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    id = User.objects.get(username = request.user).id
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(**{"author_id": id})  # Save the post with the author ID
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
def update_post(request):
    pass


@api_view(['POST', 'DELETE'])
def delete_post(request, pk):
    post = Posts.objects.get(id=pk)
    serializer = PostSerializer(post)
    serializer.delete()
    return Response(serializer.data)
