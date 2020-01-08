from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, TokenSerializer, UserSerializer
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@permission_classes([IsAuthenticated])
class CheckToken(APIView):
    def post(self, request):
        return Response(status=status.HTTP_200_OK, data=request.user.id)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'id': user.id}, status=status.HTTP_200_OK)


@permission_classes([])
class Register(APIView):
    def post(self, request):
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        username = email
        print(email)
        if username is None or username == "":
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Email is not provided")
        if password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="password is not provided")
        if first_name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="first_name is not provided")
        if last_name is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="last_name is not provided")
        check = User.objects.filter(username=username)
        if len(check) > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="username exists")
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        token = TokenSerializer(Token.objects.get(user=user))
        return Response(status=status.HTTP_200_OK, data={'token': token.key, 'id': user.id})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_403_FORBIDDEN, data="Not allowed")
