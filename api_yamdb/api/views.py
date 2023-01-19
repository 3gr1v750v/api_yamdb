from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status

from reviews.models import Title, Category, Genre, User

from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, ConfirmationCodeSerailizer
from .email import confirmation_code_email


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter
    http_method_names = ['patch', 'get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data['category']
            )
        )


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = ()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ConfirmationCodeView(APIView):
    """
    Проверка наличия регистрации на сайте у пользователя и соответствие
    почтового адреса тому, что был использован при регистрации.
    Ранее зарегистрированный пользователь получит письмо с кодом
    подтверждения для дальнейшего получения токена.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        user = User.objects.filter(username=username, email=email)
        serializer = ConfirmationCodeSerailizer(data=request.data)
        if serializer.is_valid() and user:
            confirmation_code = username.encode("utf-8").hex()[:10]
            confirmation_code_email(email, confirmation_code)
            return Response(
                {
                    "success": (f"Вам отправлено письмо с кодом "
                                f"подтверждения на адрес {email}")
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": ("Запрошенного username или email "
                         "не зарегистрировано.")
             },
            status=status.HTTP_400_BAD_REQUEST,
        )
