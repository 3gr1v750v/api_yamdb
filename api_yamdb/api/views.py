from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status


from reviews.models import Title, Category, Genre, User
from .utils import code_generator

from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsProfileOwner, IsAdminOnly
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    ConfirmationCodeSerailizer,
    UserSerializer)
from .email import confirmation_code_email


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['patch', 'get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data['category']
            ),
        )


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ConfirmationCodeView(APIView):
    """
    Самостоятельная регистрация пользователя на портале.
    Если данные прошли валидацию новый пользователь будет зарегистрирован и
    получит письмо с кодом подтверждения. Если пользователь был
    зарегистрирован ранее, он также получит письмо с кодом подтверждения.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        user = User.objects.filter(username=username, email=email)
        if username:
            confirmation_code = code_generator(username)
        if user:
            confirmation_code_email(email, confirmation_code)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = ConfirmationCodeSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            confirmation_code_email(email, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления пользователями.
    Можно осуществлять добавление и поиск по пользователям.
    Пользователь может дополнить данные о себе через обращение к эндпоинту
    /me/.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly, permissions.IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_name='get_user',
        permission_classes=(IsProfileOwner, permissions.IsAuthenticated)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
