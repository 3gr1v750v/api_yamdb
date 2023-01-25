from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status


from reviews.models import Title, Category, Genre, Comment, Review, User
from .utils import code_generator
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsProfileOwner, IsAdminOnly
from .serializers import (TitleSerializer, CategorySerializer,
                          GenreSerializer, CommentSerializer,
                          ReviewSerializer, ConfirmationCodeSerailizer,
                          UserSerializer, TitleViewSerializer)
from .email import confirmation_code_email


class TitleViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для работы с моделью Title.
    Разрешено частичное обновление, добавление, удаление,
    получение списка всех элементов и одного элемента.
    Доступен всем для чтения и администратору для модификации.
    Подключена фильтрация по полям: category, genre, name, year.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['patch', 'get', 'post', 'delete']

    def perform_create(self, serializer):
        """Добавляет категорию к произведению при сохранении."""
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data['category']
            ),
        )

    def perform_update(self, serializer):
        """Обновляет категорию у произведения при изменениии."""
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data['category']
            ),
        )

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleViewSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        new_queryset = Comment.objects.filter(
            review__title=title_id,
            review=review_id
        )
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        return super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        return super(CommentViewSet, self).perform_destroy(serializer)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    Эндпоинт для работы с моделью Category.
    Разрешено добавление, удаление и получение списка всех элементов.
    Доступен всем для чтения и администратору для модификации.
    Подключена фильтрация по полю: name
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
       Эндпоинт для работы с моделью Genre.
       Разрешено добавление, удаление и получение списка всех элементов.
       Доступен всем для чтения и администратору для модификации.
       Подключена фильтрация по полю: name
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        return super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        return super(ReviewViewSet, self).perform_destroy(serializer)


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
