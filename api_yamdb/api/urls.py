from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from api.views import (AdminUserViewSet, CategoryViewSet, CommentViewSet,
                       GenreViewSet, GetTokenViewSet, ReviewViewSet,
                       TitleViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

# router = routers.DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin_user')

auth_router = routers.DefaultRouter()
auth_router.register(r'signup', UserViewSet, basename='signup')
auth_router.register(r'token', GetTokenViewSet, basename='token')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_router.urls)),

    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
