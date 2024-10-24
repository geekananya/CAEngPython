from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from .models import Posts, Likes
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer, LikesSerializer


# this guy implemented his own login/register functions, and utilised drf tokens to generate tokens and verify/validate them
# and django user model to automatically hash password (but we can use an external lib for that for custom user model)



@api_view(['POST'])
def login(request):
    print("req.data", request.data)
    user = User.objects.filter(username=request.data.get('username')).first()
    print(user)
    if not user or not user.check_password(request.data.get('password')):
        return Response({"error": "Invalid Credentials"})
    # print(user.username)
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
        user = User.objects.get(username=request.data.get('username'))  # no need to be parsed by python, db purpose only
        user.set_password(request.data.get('password'))  # hashes password
        user.is_active = True
        user.save()
        print(user.password)
        token = Token.objects.create(user=user)
        print(token)
        return Response({'token': token.key, 'user': serialiser.data})

    print(serialiser)
    return Response({'error': serialiser.errors})


@api_view(['GET'])
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist) as e:
        print(e)
    return Response({"success": "Successfully logged out."},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def get_users(req):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(req, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user)
    user.delete()
    return Response(serializer.data)


@api_view(['GET'])
def welcome(request):
    return Response({"msg": "Welcome to django rest api"})


@api_view(['GET'])
def get_posts(request):
    posts = Posts.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, pk):
    post = get_object_or_404(Posts, id=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)


# protected route
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    username = User.objects.get(username = request.user).username



    serializer = PostSerializer(data=request.data, context={'author': username})      #overriding create method->called after save ig

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success response
    else:
        return Response({"error": serializer.errors})


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'PUT'])
def update_post(request, pk):
    post = Posts.objects.get(id = pk)
    if post.author_username != str(request.user):
        return Response({"error": 'Unauthorized action'})
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid() :
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def delete_post(request, pk):
    post = Posts.objects.get(id=pk)
    if post.author_username != str(request.user):
        return Response({"error": 'Unauthorized action'}, HTTP_401_UNAUTHORIZED)
    serializer = PostSerializer(post)
    post.delete()
    return Response(serializer.data)


# NOTE:
# DB model and serialiser don't always go together.
# Serialiser is only needed when we have to parse req data into model or send model through resp.

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = Posts.objects.filter(id=pk).first()

    like, created = Likes.objects.get_or_create(post=post, user=request.user)
    if created:
        post.likes_no += 1
        post.save()
        return Response('Like successful')
    else:
        return Response("Like already exists.")


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = Posts.objects.filter(id=pk).first()

    like = Likes.objects.filter(post=post, user=request.user).first()
    if not like:
        return Response({'error': 'No like found'})
    like.delete()
    post.likes_no -= 1
    post.save()
    return Response('Unlike successful')


@api_view(['GET'])
def get_likes(req):
    likes = Likes.objects.all()
    serializer = LikesSerializer(likes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_like_status(request, pk):
    post = Posts.objects.filter(id=pk).first()
    like = Likes.objects.filter(post=post, user=request.user).first()
    return Response({'isLiked': bool(like)})


@api_view(['GET'])
def search_post_by_tag(req, tag):
    filtered_posts = Posts.objects.filter(tags__icontains=tag)
    serializer = PostSerializer(filtered_posts, many=True)
    return Response(serializer.data)
