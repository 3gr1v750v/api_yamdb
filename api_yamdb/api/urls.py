from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailAuthSerializer
from .views import (
    CategoryViewSet,
    CommentViewSet,
    ConfirmationCodeView,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = 'api'


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)' r'/comments',
    CommentViewSet,
    basename='comments',
)
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        "v1/auth/signup/",
        ConfirmationCodeView.as_view(),
        name='user_obtain_code',
    ),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(serializer_class=EmailAuthSerializer),
        name='user_obtain_token',
    ),
]
