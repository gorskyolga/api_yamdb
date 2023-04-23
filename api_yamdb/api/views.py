
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title
from users.models import User

from api.permissions import IsAdmin
from api.serializers import (CategorySerializer, GenreSerializer,
                             SignUpSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user = User.objects.get_or_create(email=email, username=username)[0]
    send_mail(
        subject='Код подтверждения',
        message=default_token_generator.make_token(user),
        from_email='api_yamdb@example.com',
        recipient_list=[email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        data = {
            'confirmation_code': 'Код подтверждения не соответствует логину!'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    data = {'token': str(AccessToken.for_user(user))}
    return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = self.request.user
        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)
